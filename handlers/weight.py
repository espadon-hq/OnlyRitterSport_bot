from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database import get_weight_history, log_weight

router = Router()


class WeightForm(StatesGroup):
    value = State()


@router.message(Command("weight"))
@router.message(F.text == "⚖️ Вага")
async def cmd_weight(message: Message, state: FSMContext):
    await state.set_state(WeightForm.value)
    await message.answer("⚖️ Введи свою вагу (кг), наприклад: 82.5")


@router.message(WeightForm.value)
async def weight_value(message: Message, state: FSMContext):
    try:
        weight = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Введи число, наприклад: 82.5")
        return
    await state.clear()
    await log_weight(message.from_user.id, weight)

    history = await get_weight_history(message.from_user.id, days=7)
    trend = ""
    if len(history) >= 2:
        delta = round(weight - history[0][0], 1)
        if delta > 0:
            trend = f"\n▲ +{delta} кг за тиждень"
        elif delta < 0:
            trend = f"\n▼ {delta} кг за тиждень"
        else:
            trend = "\n→ без змін за тиждень"

    await message.answer(
        f"⚖️ <b>Збережено: {weight} кг</b>{trend}",
        parse_mode="HTML"
    )


@router.message(Command("weight_history"))
async def weight_history_cmd(message: Message):
    rows = await get_weight_history(message.from_user.id, days=30)
    if not rows:
        await message.answer("Даних поки немає. Введи /weight")
        return
    lines = [f"📅 {r[1]} — <b>{r[0]} кг</b>" for r in rows[-10:]]
    await message.answer(
        "⚖️ <b>Динаміка ваги:</b>\n\n" + "\n".join(lines),
        parse_mode="HTML"
    )