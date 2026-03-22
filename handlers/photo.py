import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import PHOTOS_DIR
from database import log_photo

router = Router()

os.makedirs(PHOTOS_DIR, exist_ok=True)


@router.message(Command("photo"))
@router.message(F.text == "📸 Фото")
async def cmd_photo(message: Message):
    await message.answer(
        "📸 Надішли фото прогресу — збережу з датою."
    )


@router.message(F.photo)
async def receive_photo(message: Message):
    from datetime import date
    today = date.today().isoformat()

    # беремо найбільше фото
    photo = message.photo[-1]
    file_id = photo.file_id

    # завантажуємо файл
    bot = message.bot
    file = await bot.get_file(file_id)
    file_path = os.path.join(PHOTOS_DIR, f"{today}_{file_id[:8]}.jpg")
    await bot.download_file(file.file_path, destination=file_path)

    await log_photo(message.from_user.id, file_id, file_path)

    await message.answer(
        f"📸 <b>Фото збережено!</b>\n\n"
        f"Дата: {today}\n"
        f"Файл: {file_path}",
        parse_mode="HTML"
    )