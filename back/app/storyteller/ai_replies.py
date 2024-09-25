## available_llms - gemini, claude, gpt
import json
import logging
import re
from datetime import datetime as dt
from datetime import timezone

import asyncpg
import requests
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.dependencies.settings import get_settings
from app.exceptions.CallAiExceptions import CallAiExceptions
from app.models.models import Images, Replies, Stories, StoryContexts
from app.repositories.stories_repository import StoriesRepository
from app.repositories.story_context_repository import StoryContextRepository
from app.s3.storage_manager import StorageManager
from app.storyteller.ai_query import AiQuery
from app.storyteller.data import INITIAL_CONTEXT
from app.storyteller.prompts import StoryPrompts
from app.storyteller.story_context_manager import StoryContextManager
from app.storyteller.storyteller_schemas import StoryContext
from app.utils.log_decorators import log_deco
from app.utils.loggers import story_logger as log

# from config.db import async_session as session_factory

BATCH_SIZE = 5
MAX_IMAGE_PROMPT_LENGTH = 1000
NUMBER_OF_REPLIES_TO_USE_FOR_PROMPT = 5
MAX_REPLY_LENGTH = 512  # max length of reply that can be stored in db
logger = logging.getLogger("App")
settings = get_settings()

echo_enabled = settings.app.environment == "development"


engine = create_async_engine(
    settings.db.async_sqlalchemy_database_uri,
    **settings.db.async_sqlalchemy_engine_options,
    echo=False,
)
session_factory = async_sessionmaker(engine, expire_on_commit=settings.db.expire_on_commit)


class AiReplies:
    def __init__(self, available_llms: list, story_id: int):
        self.story_id: int = story_id
        self.current_llm_index: int = 0  ## current llm to use for round
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

    async def start(self) -> None:
        await self.retrieve_story()
        await self.select_llm()
        await self.retrieve_prev_replies()
        await self.retrieve_and_set_context()
        await self.set_new_reply_prompt()
        await self.get_new_reply()
        self.update_batch_info()
        await self.add_image_to_story()
        await self.update_db_with_new_reply()
        await self.update_context()

    async def update_context(self) -> None:
        log.info("-----------------Updating context-----------------")
        if self.number_in_batch == BATCH_SIZE and self.story.story_type == "wc":
            new_reply = self.new_reply if self.new_reply else ""
            excerpt = self.prev_replies_string + new_reply
            self.context_manager.update_story_excerpt(excerpt)
            await self.context_manager.update_story_context()
            async with session_factory() as session:
                await StoryContextRepository.add_new_context_entry_to_db(
                    session, self.context_manager.context, self.story_id
                )

    async def retrieve_story(self) -> None:
        async with session_factory() as session:
            self.story: Stories = await StoriesRepository.retrieve_story_by_id(
                session, self.story_id
            )

    async def set_new_reply_prompt(self) -> None:
        if self.prev_replies is None:
            await self.create_initial_prompt()
        else:
            self.prev_replies_string = "".join([reply.reply for reply in self.prev_replies])
            await self.create_prompt()

    async def retrieve_and_set_context(self) -> None:
        if self.story.story_type == "wc":  ##with context
            db_context_response = await self.retrieve_current_context()
            if db_context_response is None:
                log.debug("-------------No context found-----------------")
                db_context_response = await self.create_initial_context()
            log.debug(
                "---------------------------------------db_context_response %s",
                json.dumps(db_context_response.to_dict(), indent=4),
            )
            context_dict = db_context_response.to_dict()
            self.check_context_data_in_details(context_dict["context"])
            self.context_manager = StoryContextManager(StoryContext(**context_dict["context"]), "")

    def check_context_data_in_details(self, context: dict) -> bool:
        # log.info("CONTEXT %s", context)
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("Story Rules %s", context["rules"])
        # rules = Rules(**context["rules"])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("Current context %s", context["currentContext"])
        # current_context = CurrentContext(**context["currentContext"])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("narration %s", json.dumps(context["narration"], indent=4))
        # narration = Narrator(**context["narration"]["narrators"][0])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("themes %s", json.dumps(context["themes"], indent=4))
        # themes = context["themes"]
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("sub plots %s", json.dumps(context["subPlots"], indent=4))
        # sub_plots = PlotPoint(**context["subPlots"][0])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("main plots %s", json.dumps(context["mainPlots"], indent=4))
        # main_plots = PlotPoint(**context["mainPlots"][0])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("characters %s", json.dumps(context["characters"], indent=4))
        # characters = AllCharacters(**context["characters"])
        # log.info("!!!!!!-------------------------------------------------------!!!!!!")
        # log.info("settings %s", json.dumps(context["setting"], indent=4))
        # settings = Setting(**context["setting"])

        return True

    async def retrieve_prev_replies(self) -> None:
        self.prev_replies = await self.retrieve_latest_n_db_entries(
            NUMBER_OF_REPLIES_TO_USE_FOR_PROMPT
        )

    async def create_initial_prompt(self) -> None:
        self.prompt = """You are the first player in a game of exquisite corpse.
        Please write a sentence to start the story."""

    async def select_llm(self) -> None:
        self.current_llm = self.available_llms[self.current_llm_index]
        self.current_llm_index += 1
        if self.current_llm_index + 1 > len(self.available_llms):
            self.current_llm_index = 0

    async def create_prompt(self) -> None:
        if self.prev_replies_string is None:
            raise CallAiExceptions.NoPreviousReplyError
        if self.story.story_type == "wc":
            story_context = await self.context_manager.create_context_summary()
            self.prompt = StoryPrompts.story_prompt_with_context(
                story_context, self.prev_replies_string
            )
        else:
            self.prompt = StoryPrompts.story_prompt_without_context(self.prev_replies_string)
        log.info("Prompt created , %s", self.prompt)

    def check_if_reply_is_too_long_and_fix(self) -> None:
        if self.new_reply and len(self.new_reply) > MAX_REPLY_LENGTH:
            split_reply = self.new_reply.split(".")
            self.new_reply = split_reply[0] + "."

    def check_if_prompt_is_too_long_and_fix_it(self) -> None:
        log.info("Prompt length: %s", len(self.image_prompt))
        if self.image_prompt and len(self.image_prompt) > MAX_IMAGE_PROMPT_LENGTH:
            split_prompt = self.image_prompt.split(".")
            self.image_prompt = split_prompt[0] + "."
            log.info("removed extra text from prompt %s", self.image_prompt)

    async def update_db_with_new_reply(self) -> None:
        self.check_if_reply_is_too_long_and_fix()
        model_version_used = self.model_versions_dict[self.current_llm]
        if model_version_used is None:
            msg = "Unable to find model version to update db with"
            raise CallAiExceptions.InvalidLlmError(msg)
        new_reply = Replies(
            reply=self.new_reply,
            model=self.current_llm,
            version=model_version_used,
            batch_id=self.batch_id,
            number_in_batch=self.number_in_batch,
            story_id=self.story_id,
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
            story_id=self.story_id,
        )
        async with session_factory() as session:
            session.add(new_image)
            await session.commit()

    def reset_llm_index(self) -> None:
        self.current_llm_index = (
            len(self.available_llms) if self.current_llm_index == 0 else self.current_llm_index - 1
        )

    # TODO: select store which llms have been used in a db so
    # that we can use all llms before repeating

    async def retrieve_current_context(self) -> StoryContexts:
        async with session_factory() as session:
            return await StoryContextRepository.retrieve_story_context(session, self.story_id)

    async def create_initial_context(self) -> StoryContexts:
        new_context = StoryContexts(story_id=self.story_id, context=INITIAL_CONTEXT)
        async with session_factory() as session:
            session.add(new_context)
            await session.commit()
        return new_context

    async def add_image_to_story(self) -> None:
        if self.number_in_batch == BATCH_SIZE:
            self.create_image_prompt()
            await self.generate_image()
            await self.save_image_to_s3()
            await self.update_db_with_new_image()

    async def generate_image(self) -> None:
        ai_query = AiQuery(self.current_llm, self.image_prompt)
        image_url = await ai_query.create_image(self.image_prompt)
        self.image_url = image_url

    async def save_image_to_s3(self) -> None:
        if self.image_url is None:
            raise CallAiExceptions.NoImageUrlError
        image = await download_image(self.image_url)
        img_name = sanitize_filename(f"batch_{self.batch_id}_{dt.now(timezone.utc)}.png")
        await StorageManager.upload_file_to_s3(image, "story-images", img_name)
        self.img_uri = "story-images/" + img_name
        self.img_name = img_name

    def create_image_prompt(self) -> None:
        self.image_prompt = f""" You are a storybook illustrator.  Create an illustration for the
        following passage: {self.prev_replies_string}"""
        self.check_if_prompt_is_too_long_and_fix_it()

    def update_batch_info(self) -> None:
        if len(self.prev_replies) > 0 and self.prev_replies[-1] is not None:
            self.batch_id = (
                self.prev_replies[-1].batch_id + 1
                if self.prev_replies[-1].number_in_batch == BATCH_SIZE
                else self.prev_replies[-1].batch_id
            )
            self.number_in_batch = (
                self.prev_replies[-1].number_in_batch + 1
                if self.prev_replies[-1].number_in_batch < BATCH_SIZE
                else 1
            )
        else:
            self.batch_id = 1
            self.number_in_batch = 1

    @log_deco
    async def retrieve_latest_n_db_entries(self, qty_replies: int = 1) -> list[Replies]:
        async with session_factory() as session:
            result = await session.execute(
                select(Replies)
                .filter(Replies.story_id == self.story_id)
                .order_by(desc(Replies.time_created))
                .limit(qty_replies)
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
        log.info("--------------------New reply created--------------, \n \n %s", new_reply)


async def download_image(url: str) -> bytes:
    r = requests.get(url, timeout=5)  # noqa: ASYNC210
    r.raise_for_status()
    return r.content


def sanitize_filename(filename: str) -> str:
    # Replace spaces with underscores and remove colons
    return re.sub(r"[^A-Za-z0-9\-_.]", "_", filename)
