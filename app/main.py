import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("ENV_BOT_TOKEN",default=DefaultBotProperties(parse_mode=ParseMode.HTML))

if not BOT_TOKEN:
    raise ValueError("Переменная ENV_BOT_TOKEN не задана на хостинге!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer(
		"Здарова.\n\n"
		"Я tac1ical OSINT, инструмент для сбора и анализа информации из открытых источников.\n\n"
		"Доступные команды:\n"
		"/ip — Информация по IP-адресу\n"
		"/nick — Поиск публичных профилей по никнейму\n"
		"/help — Справка\n\n"
		"Ограничения:\n"
		"Базовый лимит: 3 запроса в сутки.\n\n"
		"[Инструмент предназначен исключительно для исследовательских задач в рамках действующего законодательства.]\n"
	)

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
