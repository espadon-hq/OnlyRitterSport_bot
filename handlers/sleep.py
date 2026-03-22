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

from database import log_sleep

router = Router()


class SleepForm(StatesGroup):
    hours = State()
    quality = State()


def _quality_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text=f"{'⭐' * i}", callback_data=f"sleep_q:{i}")
        for i in range(1, 6)
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("sleep"))
@router.message(F.text == "😴 Сон")
async def cmd_sleep(message: Message, state: FSMContext):
    await state.set_state(SleepForm.hours)
    await message.answer("😴 Скільки годин спав? (наприклад: 7.5)")


@router.message(SleepForm.hours)
async def sleep_hours(message: Message, state: FSMContext):
    try:
        hours = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Введи число, наприклад: 7.5")
        return
    await state.update_data(hours=hours)
    await state.set_state(SleepForm.quality)
    await message.answer(
        "Оціни якість сну:",
        reply_markup=_quality_keyboard()
    )


@router.callback_query(F.data.startswith("sleep_q:"), SleepForm.quality)
async def sleep_quality(callback: CallbackQuery, state: FSMContext):
    quality = int(callback.data.split(":")[1])
    data = await state.get_data()
    await state.clear()
    await log_sleep(callback.from_user.id, data["hours"], quality)
    await callback.message.edit_text(
        f"😴 <b>Збережено!</b>\n\n"
        f"Годин: {data['hours']}\n"
        f"Якість: {'⭐' * quality}",
        parse_mode="HTML"
    )
    await callback.answer()
    