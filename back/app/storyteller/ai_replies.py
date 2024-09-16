## available_llms - gemini, claude, gpt
import logging
import re
from datetime import datetime as dt
from datetime import timezone
from pathlib import Path

import asyncpg
import requests
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.dependencies.settings import get_settings
from app.exceptions.CallAiExceptions import CallAiExceptions
from app.models.images import Images
from app.models.replies import Replies
from app.s3.storage_manager import StorageManager
from app.storyteller.ai_query import AiQuery
from app.utils.log_decorators import log_deco

# from config.db import async_session as session_factory

BATCH_SIZE = 5
NUMBER_OF_REPLIES_TO_USE_FOR_PROMPT = 5
MAX_REPLY_LENGTH = 512  # max length of reply that can be stored in db
logger = logging.getLogger("App")
settings = get_settings()

echo_enabled = settings.app.environment == "development"


engine = create_async_engine(
    "postgresql+asyncpg://user:1234@localhost:5431/db",
    **settings.db.async_sqlalchemy_engine_options,
    echo=False,
)
session_factory = async_sessionmaker(
    engine,
    expire_on_commit=settings.db.expire_on_commit,
)


class AiReplies:
    def __init__(self, available_llms: list):
        self.current_llm_index: int = 0  ## current llm to use for round
        self.prev_reply: Replies | None = (
            None  ## previous reply from llm to be used to prompt new llm
        )
        self.prompt: str | None = None
        self.new_reply: str | None = None  ## new reply from llm
        self.llms_in_round: list[
            str
        ] = []  ## keep track of which llms have been queried in current round
        self.available_llms: list[str] = available_llms  ## list of all available llms
        self.settings = get_settings().ai

        self.model_versions_dict: dict = {
            "llama": self.settings.llama.main_model,
            "gpt": self.settings.open_ai.main_model,
            "claude": self.settings.anthropic.main_model,
            "mistral": self.settings.mistral.main_model,
            "gemini": self.settings.gemini.main_model,
        }

    @log_deco
    async def create_initial_prompt(self) -> None:
        self.prompt = """You are the first player in a game of exquisite corpse.
        Please write a sentence to start the story."""

    @log_deco
    async def select_llm(self) -> None:
        self.current_llm = self.available_llms[self.current_llm_index]
        self.current_llm_index += 1
        if self.current_llm_index + 1 > len(self.available_llms):
            self.current_llm_index = 0

    @log_deco
    async def create_prompt(self) -> None:
        if self.prev_replies_string is None:
            raise CallAiExceptions.NoPreviousReplyError
        self.prompt = f"""You are playing a game of exquisite corpse. The previous 5 sentences
        written by players are:\n
        {self.prev_replies_string}.\n Please write the next sentence to continue the story.
        Only reply with the next sentence you would like to add to the story.
        Do not include any markdown or formatting or anything other than the
        sentence that continues the story. You must not reply with anything other than the next
        sentence."""

    def check_if_reply_is_too_long_and_fix(self) -> None:
        if self.new_reply and len(self.new_reply) > MAX_REPLY_LENGTH:
            split_reply = self.new_reply.split(".")
            self.new_reply = split_reply[0] + "."

    @log_deco
    async def update_db_with_new_reply(self) -> None:
        self.check_if_reply_is_too_long_and_fix()
        model_version_used = self.model_versions_dict[self.current_llm]
        if model_version_used is None:
            msg = "Unable to find model version to update db with"
            raise CallAiExceptions.InvalidLlmError(
                msg,
            )
        new_reply = Replies(
            reply=self.new_reply,
            model=self.current_llm,
            version=model_version_used,
            batch_id=self.batch_id,
            number_in_batch=self.number_in_batch,
        )
        async with session_factory() as session:
            try:
                session.add(new_reply)
                await session.commit()
            except asyncpg.exceptions.StringDataRightTruncationError as e:
                self.reset_llm_index()
                raise CallAiExceptions.ResponseTooLongError(self.current_llm) from e

    async def update_db_with_new_image(self) -> None:
        new_image = Images(
            image_url=self.img_uri,
            batch_id=self.batch_id,
            img_model=self.settings.open_ai.image_model,
            title=self.img_name,
        )
        async with session_factory() as session:
            session.add(new_image)
            await session.commit()

    def reset_llm_index(self) -> None:
        self.current_llm_index = (
            len(self.available_llms) if self.current_llm_index == 0 else self.current_llm_index - 1
        )

    @log_deco
    async def start(self) -> None:
        print("starting")
        await self.select_llm()
        reply_list = await self.retrieve_latest_n_db_entries()
        self.prev_reply = reply_list[0] if reply_list else None
        self.prev_replies = await self.retrieve_latest_n_db_entries(
            NUMBER_OF_REPLIES_TO_USE_FOR_PROMPT,
        )
        if self.prev_reply is None:
            await self.create_initial_prompt()

        else:
            if self.prev_replies is None:
                raise CallAiExceptions.NoPreviousReplyError("No previous replies found")
            self.prev_replies_string = "".join([reply.reply for reply in self.prev_replies])
            await self.create_prompt()
        await self.get_new_reply()
        self.update_batch_info()
        if self.number_in_batch == BATCH_SIZE:
            self.create_image_prompt()
            await self.generate_image()
            await self.save_image_to_s3()
            await self.update_db_with_new_image()
        await self.update_db_with_new_reply()

    async def generate_image(self) -> None:
        ai_query = AiQuery(self.current_llm, self.image_prompt)
        image_url = await ai_query.create_image(self.image_prompt)
        self.image_url = image_url

    async def save_image_to_s3(self) -> None:
        if self.image_url is None:
            raise CallAiExceptions.NoImageUrlError
        image = await download_image(self.image_url)
        img_name = f"batch_{self.batch_id}_{dt.now(timezone.utc)}.png"
        img_name = sanitize_filename(img_name)
        directory_path = Path("temp").resolve()
        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)
        img_path = Path(directory_path) / img_name
        print("img_path", img_path)
        # async with await anyio.open_file(img_path, "wb") as f:
        #     await f.write(image)
        await StorageManager.upload_file_to_s3(image, "story-images", img_name)
        self.img_uri = "story-images/" + img_name
        self.img_name = img_name

    def create_image_prompt(self) -> None:
        self.image_prompt = f""" You are a storybook illustrator.  Create an illustration for the
        following passage: {self.prev_replies_string}"""

    def update_batch_info(self) -> None:
        if self.prev_reply is not None:
            self.batch_id = (
                self.prev_reply.batch_id + 1
                if self.prev_reply.number_in_batch == BATCH_SIZE
                else self.prev_reply.batch_id
            )
            self.number_in_batch = (
                self.prev_reply.number_in_batch + 1
                if self.prev_reply.number_in_batch < BATCH_SIZE
                else 1
            )
        else:
            self.batch_id = 1
            self.number_in_batch = 1

    @log_deco
    async def retrieve_latest_n_db_entries(self, qty_replies: int = 1) -> list[Replies]:
        async with session_factory() as session:
            result = await session.execute(
                select(Replies).order_by(desc(Replies.time_created)).limit(qty_replies),
            )
            return list(result.scalars().all())

    @log_deco
    async def get_new_reply(self) -> None:
        if self.current_llm is None:
            raise CallAiExceptions.NoLlmSelectedError
        if self.prompt is None:
            raise CallAiExceptions.NoPromptError
        ai_query = AiQuery(self.current_llm, self.prompt)
        new_reply: str = await ai_query.query()
        self.new_reply = new_reply


async def download_image(url: str) -> bytes:
    r = requests.get(url, timeout=5)  # noqa: ASYNC210
    r.raise_for_status()
    return r.content


def sanitize_filename(filename: str) -> str:
    # Replace spaces with underscores and remove colons
    return re.sub(r"[^A-Za-z0-9\-_.]", "_", filename)
