import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from config import MY_TELEGRAM_ID, SUPPLEMENTS, TIMEZONE

logger = logging.getLogger(__name__)
tz = timezone(TIMEZONE)


async def remind_morning(bot):
    await bot.send_message(
        MY_TELEGRAM_ID,
        "🌅 <b>Доброго ранку!</b>\n\n"
        "Зафіксуй:\n"
        "• /weight — вага\n"
        "• /sleep — як спав\n"
        "• /mood — настрій",
        parse_mode="HTML"
    )


async def remind_supplements(bot, time_slot: str, label: str):
    names = [s["name"] for s in SUPPLEMENTS if time_slot in s.get("times", [])]
    if not names:
        return
    lines = "\n".join(f"• {n}" for n in names)
    await bot.send_message(
        MY_TELEGRAM_ID,
        f"💊 <b>БАДи — {label}</b>\n\n{lines}\n\n/supplements",
        parse_mode="HTML"
    )


async def remind_training(bot):
    await bot.send_message(
        MY_TELEGRAM_ID,
        "🏋️ Тренувався сьогодні? Зафіксуй: /training",
        parse_mode="HTML"
    )


async def remind_mood_evening(bot):
    await bot.send_message(
        MY_TELEGRAM_ID,
        "🌙 Як пройшов день? Зафіксуй настрій: /mood",
        parse_mode="HTML"
    )


async def remind_summary(bot):
    await bot.send_message(
        MY_TELEGRAM_ID,
        "📊 Переглянь підсумок дня: /summary",
        parse_mode="HTML"
    )


async def remind_weekly_photo(bot):
    await bot.send_message(
        MY_TELEGRAM_ID,
        "📸 <b>Неділя — час фото прогресу!</b>\n\nНадішли фото або /photo",
        parse_mode="HTML"
    )


async def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=tz)

    scheduler.add_job(remind_morning, CronTrigger(hour=7, minute=0, timezone=tz), args=[bot])
    scheduler.add_job(remind_supplements, CronTrigger(hour=8, minute=0, timezone=tz), args=[bot, "08:00", "ранок"])
    scheduler.add_job(remind_supplements, CronTrigger(hour=13, minute=0, timezone=tz), args=[bot, "13:00", "день"])
    scheduler.add_job(remind_training, CronTrigger(hour=18, minute=0, timezone=tz), args=[bot])
    scheduler.add_job(remind_supplements, CronTrigger(hour=21, minute=0, timezone=tz), args=[bot, "21:00", "вечір"])
    scheduler.add_job(remind_mood_evening, CronTrigger(hour=21, minute=5, timezone=tz), args=[bot])
    scheduler.add_job(remind_summary, CronTrigger(hour=22, minute=30, timezone=tz), args=[bot])
    scheduler.add_job(remind_weekly_photo, CronTrigger(day_of_week="sun", hour=10, minute=0, timezone=tz), args=[bot])

    logger.info("Scheduler ready.")
    return scheduler