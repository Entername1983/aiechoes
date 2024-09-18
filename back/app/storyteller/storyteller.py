import asyncio
import json
import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.dependencies.settings import get_settings
from app.storyteller.ai_replies import AiReplies

settings = get_settings()
ai_replies = AiReplies(settings.story.available_llms)


async def job_function() -> None:
    current_time = datetime.now(timezone.utc)
    print(f"Job executed at {current_time} UTC")  # noqa: T201
    await ai_replies.start()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("Storyteller")

scheduler = AsyncIOScheduler()

trigger = CronTrigger(second="10")


scheduler.add_job(job_function, trigger)


settings = get_settings()

settings_dict = settings.model_dump()


async def main() -> None:
    log.info("-----------------Starting Storyteller-----------------")
    log.info(json.dumps(settings.model_dump(), indent=4))
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
