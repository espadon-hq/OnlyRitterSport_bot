from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import SUPPLEMENTS
from database import get_daily_summary

router = Router()


@router.message(Command("summary"))
@router.message(F.text == "📊 Підсумок дня")
async def cmd_summary(message: Message):
    data = await get_daily_summary(message.from_user.id)

    # БАДи
    taken = {r[0] for r in data["supplements"] if r[1] == 1}
    total = len(SUPPLEMENTS)
    done = len(taken)
    sup_line = f"💊 БАДи: {done}/{total} {'✅' if done == total else '⚠️'}"

    # Тренування
    if data["trainings"]:
        t = data["trainings"][0]
        train_line = f"🏋️ Тренування: {t[0]} {t[1]} хв ✅"
    else:
        train_line = "🏋️ Тренування: не зафіксовано ❌"

    # Вага
    if data["weight"]:
        weight_line = f"⚖️ Вага: {data['weight'][0]} кг ✅"
    else:
        weight_line = "⚖️ Вага: не зафіксована ❌"

    # Сон
    if data["sleep"]:
        s = data["sleep"]
        weight_line2 = f"😴 Сон: {s[0]} год, якість {'⭐' * s[1]}"
    else:
        weight_line2 = "😴 Сон: не зафіксовано ❌"

    # Настрій
    if data["mood"]:
        m = data["mood"][0]
        mood_line = f"😊 Настрій: {m[0]}/5 | Енергія: {m[1]}/5"
    else:
        mood_line = "😊 Настрій: не зафіксовано ❌"

    await message.answer(
        f"📊 <b>Підсумок дня</b>\n\n"
        f"{sup_line}\n"
        f"{train_line}\n"
        f"{weight_line}\n"
        f"{weight_line2}\n"
        f"{mood_line}",
        parse_mode="HTML"
    )