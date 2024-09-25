import asyncio
import json
import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.dependencies.settings import get_settings
from app.storyteller.ai_replies import AiReplies
from app.utils.loggers import story_logger as log

settings = get_settings()
ai_replies = AiReplies(settings.story.available_llms, 2)


async def job_function() -> None:
    log.info("Job executed at %s UTC", datetime.now(timezone.utc))
    await ai_replies.start()


scheduler = AsyncIOScheduler()


if settings.app.environment == "development":
    trigger = CronTrigger(second=30)
else:
    trigger = CronTrigger(minute=settings.story.interval_min)


scheduler.add_job(job_function, trigger)


settings = get_settings()

settings_dict = settings.model_dump()

# Set the log level for httpx and httpcore to WARNING or ERROR
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def main() -> None:
    log.info("-----------------Starting Storyteller-----------------")

    log.info(json.dumps(settings.model_dump(), indent=4))
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
