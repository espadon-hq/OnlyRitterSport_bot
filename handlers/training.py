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

from database import log_training

router = Router()

TRAINING_TYPES = ["Сила", "Кардіо", "HIIT", "Йога", "Інше"]


class TrainingForm(StatesGroup):
    type = State()
    duration = State()
    notes = State()


def _type_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=t, callback_data=f"train:{t}")] for t in TRAINING_TYPES]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("training"))
@router.message(F.text == "🏋️ Тренування")
async def cmd_training(message: Message, state: FSMContext):
    await state.set_state(TrainingForm.type)
    await message.answer(
        "🏋️ <b>Нове тренування</b>\n\nОбери тип:",
        reply_markup=_type_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("train:"), TrainingForm.type)
async def training_type(callback: CallbackQuery, state: FSMContext):
    t = callback.data.split(":", 1)[1]
    await state.update_data(type=t)
    await state.set_state(TrainingForm.duration)
    await callback.message.edit_text(
        f"Тип: <b>{t}</b>\n\nСкільки хвилин? (наприклад: 60)",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(TrainingForm.duration)
async def training_duration(message: Message, state: FSMContext):
    try:
        duration = int(message.text.strip())
    except ValueError:
        await message.answer("Введи число хвилин, наприклад: 60")
        return
    await state.update_data(duration=duration)
    await state.set_state(TrainingForm.notes)
    await message.answer("Нотатки? (або напиши «-» щоб пропустити)")


@router.message(TrainingForm.notes)
async def training_notes(message: Message, state: FSMContext):
    notes = "" if message.text.strip() == "-" else message.text.strip()
    data = await state.get_data()
    await state.clear()
    await log_training(message.from_user.id, data["type"], data["duration"], notes)
    await message.answer(
        f"🏋️ <b>Збережено!</b>\n\n"
        f"Тип: {data['type']}\n"
        f"Тривалість: {data['duration']} хв"
        + (f"\nНотатки: {notes}" if notes else ""),
        parse_mode="HTML"
    )