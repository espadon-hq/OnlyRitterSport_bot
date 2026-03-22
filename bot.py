import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from config import BOT_TOKEN
from database import init_db
from handlers.supplements import router as sup_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(sup_router)

MENU = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💊 БАДи"), KeyboardButton(text="🏋️ Тренування")],
    [KeyboardButton(text="⚖️ Вага"),  KeyboardButton(text="😴 Сон")],
    [KeyboardButton(text="😊 Настрій"), KeyboardButton(text="📸 Фото")],
    [KeyboardButton(text="📊 Підсумок дня")],
], resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт! 👋 Обери що записати:", reply_markup=MENU)

async def main():
    await init_db()
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())