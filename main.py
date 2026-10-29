import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("tac1ical OSINT на связи.\nЯ готов к работе.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - Приветствие\n/help - Помощь\n/ip - Скоро...")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Эхо: {message.text}")

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())