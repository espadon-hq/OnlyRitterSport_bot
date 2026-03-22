from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import SUPPLEMENTS
from database import get_supplements_today, log_supplement

router = Router()


def _build_keyboard(taken_names: set) -> InlineKeyboardMarkup:
    buttons = []
    for s in SUPPLEMENTS:
        name = s["name"]
        check = "✅" if name in taken_names else "⬜"
        buttons.append([InlineKeyboardButton(
            text=f"{check} {name} — {s['dose']}",
            callback_data=f"sup:{name}"
        )])
    buttons.append([InlineKeyboardButton(text="💾 Зберегти", callback_data="sup:done")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("supplements"))
@router.message(F.text == "💊 БАДи")
async def cmd_supplements(message: Message):
    rows = await get_supplements_today(message.from_user.id)
    taken = {r[0] for r in rows if r[1] == 1}
    await message.answer(
        "💊 <b>БАДи на сьогодні</b>\n\nНатискай щоб відмітити прийом:",
        reply_markup=_build_keyboard(taken),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("sup:"))
async def toggle_supplement(callback: CallbackQuery):
    value = callback.data.split(":", 1)[1]

    if value == "done":
        rows = await get_supplements_today(callback.from_user.id)
        taken = {r[0] for r in rows if r[1] == 1}
        total = len(SUPPLEMENTS)
        done = len(taken)
        await callback.message.edit_text(
            f"💊 <b>Збережено!</b>\n\n"
            f"Прийнято: {done}/{total} {'🎉' if done == total else ''}",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    name = value
    rows = await get_supplements_today(callback.from_user.id)
    taken = {r[0] for r in rows if r[1] == 1}
    new_state = name not in taken
    await log_supplement(callback.from_user.id, name, new_state)

    rows = await get_supplements_today(callback.from_user.id)
    taken = {r[0] for r in rows if r[1] == 1}
    await callback.message.edit_reply_markup(reply_markup=_build_keyboard(taken))
    await callback.answer("✅ Прийнятий" if new_state else "↩️ Знято")