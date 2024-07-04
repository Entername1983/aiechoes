import asyncio
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dependencies.settings import get_settings
from storyteller.ai_replies import AiReplies

settings = get_settings()
ai_replies = AiReplies(settings.story.available_llms)


async def job_function():
    current_time = datetime.now(timezone.utc)
    print(f"Job executed at {current_time} UTC")
    await ai_replies.start()


scheduler = AsyncIOScheduler()

trigger = CronTrigger(second="10")
# trigger = CronTrigger(minute=f"*/{settings.story.interval_min}", second="0")


scheduler.add_job(job_function, trigger)


async def main():
    print("Starting scheduler...")
    print(f"Interval is {settings.story.interval_min}")
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
