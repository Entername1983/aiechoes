## available_llms - gemini, claude, gpt


from config.db import async_session as session_factory
from models.replies import Replies
from sqlalchemy import desc, select
from storyteller.ai_query import AiQuery
from utils.log_decorators import log_deco


class AiReplies:
    def __init__(self, available_llms: list):
        self.current_llm_index: int = 0  ## current llm to use for round
        self.prev_reply: str | None = (
            None  ## previous reply from llm to be used to prompt new llm
        )
        self.prompt: str | None = None
        self.new_reply: str | None = None  ## new reply from llm
        self.llms_in_round: list[
            str
        ] = []  ## keep track of which llms have been queried in current round
        self.available_llms: list[str] = available_llms  ## list of all available llms

    @log_deco
    async def create_initial_prompt(self):
        self.prompt = "You are the first player in a game of exquisite corpse. Please write a sentence to start the story."

    @log_deco
    async def select_llm(self):
        self.current_llm = self.available_llms[self.current_llm_index]
        self.current_llm_index += 1
        if self.current_llm_index + 1 > len(self.available_llms):
            self.current_llm_index = 0

    @log_deco
    async def create_prompt(self):
        self.prompt = f"You are playing a game of exquisite corpse. The previous player wrote: {self.prev_reply}. Please write the next sentence to continue the story.  Only reply with the next sentence you would like to add to the story.  Do not include any markdown or formatting or anything other than the sentence that continues the story."

    @log_deco
    async def update_db_with_new_reply(self):
        new_reply = Replies(reply=self.new_reply, model=self.current_llm)
        print(new_reply.__repr__())
        async with session_factory() as session:
            session.add(new_reply)
            await session.commit()

    @log_deco
    async def start(self):
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
                select(Replies).order_by(desc(Replies.time_created)).limit(1)
            )
            reply = result.scalars().first()
            return reply

    @log_deco
    async def get_new_reply(self):
        if self.current_llm is None:
            raise ValueError("current_llm is None")
        if self.prompt is None:
            raise ValueError("prompt is None")
        ai_query = AiQuery(self.current_llm, self.prompt)
        new_reply: str = await ai_query.query()
        self.new_reply = new_reply
