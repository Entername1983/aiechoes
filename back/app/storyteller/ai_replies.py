## available_llms - gemini, claude, gpt


from config.db import async_session as session_factory
from models.replies import Replies
from sqlalchemy import desc, select
from storyteller.ai_query import AiQuery
from utils.log_decorators import log_deco

from app.dependencies.settings import get_settings
from app.exceptions.CallAiExceptions import CallAiExceptions


class AiReplies:
    def __init__(self, available_llms: list):
        self.current_llm_index: int = 0  ## current llm to use for round
        self.prev_reply: str | None = None  ## previous reply from llm to be used to prompt new llm
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
        self.prompt = f"""You are playing a game of exquisite corpse. The previous player wrote:
        {self.prev_reply}. Please write the next sentence to continue the story.
        Only reply with the next sentence you would like to add to the story.
        Do not include any markdown or formatting or anything other than the
        sentence that continues the story."""

    @log_deco
    async def update_db_with_new_reply(self) -> None:
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
        )
        async with session_factory() as session:
            session.add(new_reply)
            await session.commit()

    @log_deco
    async def start(self) -> None:
        print("starting")
        await self.select_llm()
        reply = await self.retrieve_latest_single_db_entry()
        if reply is None:
            await self.create_initial_prompt()
        else:
            self.prev_reply = reply.reply
            await self.create_prompt()
        await self.get_new_reply()
        await self.update_db_with_new_reply()

    @log_deco
    async def retrieve_latest_single_db_entry(self) -> Replies | None:
        async with session_factory() as session:
            result = await session.execute(
                select(Replies).order_by(desc(Replies.time_created)).limit(1),
            )
            return result.scalars().first()

    @log_deco
    async def get_new_reply(self) -> None:
        if self.current_llm is None:
            raise CallAiExceptions.NoLlmSelectedError
        if self.prompt is None:
            raise CallAiExceptions.NoPromptError
        ai_query = AiQuery(self.current_llm, self.prompt)
        new_reply: str = await ai_query.query()
        self.new_reply = new_reply
