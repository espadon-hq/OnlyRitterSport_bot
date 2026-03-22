from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import log_mood

router = Router()


class MoodForm(StatesGroup):
    mood = State()
    energy = State()


def _rating_keyboard(prefix: str) -> InlineKeyboardMarkup:
    labels = {"1": "😞", "2": "😕", "3": "😐", "4": "🙂", "5": "😄"}
    buttons = [[
        InlineKeyboardButton(text=f"{emoji} {i}", callback_data=f"{prefix}:{i}")
        for i, emoji in labels.items()
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("mood"))
@router.message(F.text == "😊 Настрій")
async def cmd_mood(message: Message, state: FSMContext):
    await state.set_state(MoodForm.mood)
    await message.answer(
        "😊 <b>Як настрій?</b>",
        reply_markup=_rating_keyboard("mood"),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("mood:"), MoodForm.mood)
async def mood_value(callback: CallbackQuery, state: FSMContext):
    value = int(callback.data.split(":")[1])
    await state.update_data(mood=value)
    await state.set_state(MoodForm.energy)
    await callback.message.edit_text(
        "⚡ <b>Який рівень енергії?</b>",
        reply_markup=_rating_keyboard("energy"),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("energy:"), MoodForm.energy)
async def energy_value(callback: CallbackQuery, state: FSMContext):
    value = int(callback.data.split(":")[1])
    data = await state.get_data()
    await state.clear()

    mood = data["mood"]
    energy = value

    # визначаємо час доби
    from datetime import datetime

    from pytz import timezone
    hour = datetime.now(timezone("Europe/Kyiv")).hour
    time_of_day = "ранок" if hour < 12 else "вечір" if hour >= 18 else "день"

    await log_mood(callback.from_user.id, mood, energy, time_of_day)

    emojis = {1: "😞", 2: "😕", 3: "😐", 4: "🙂", 5: "😄"}
    await callback.message.edit_text(
        f"✅ <b>Збережено!</b>\n\n"
        f"Настрій: {emojis[mood]} {mood}/5\n"
        f"Енергія: ⚡ {energy}/5\n"
        f"Час: {time_of_day}",
        parse_mode="HTML"
    )
    await callback.answer()