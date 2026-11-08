import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from getIP import getInfoByIP
from lookup import check_username_maigret

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("ENV_BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer(
		"Здарова.\n\n"
		"Я tac1ical OSINT, инструмент для сбора и анализа информации из открытых источников.\n\n"
		"Доступные команды:\n"
		"/ip - Информация по IP-адресу\n"
		"/nick - Поиск публичных профилей по никнейму\n"
		"/help - Справка\n\n"
		"Ограничения:\n"
		"Базовый лимит: 3 запроса в сутки.\n\n"
		"<i>Инструмент предназначен исключительно для исследовательских задач.</i>"
	)

@dp.message(Command("ip"))
async def cmd_ip(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /ip <адрес>")
        return      
    ip_address = args[1]
    msg = await message.answer("Ищу информацию...")
    data = getInfoByIP(ip_address)
    formatted_text = json.dumps(data, indent=2, ensure_ascii=False)
    await msg.edit_text(f"<code>{formatted_text}</code>")


@dp.message(Command("nick"))
async def cmd_nick(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /nick <никнейм>")
        return      
    username = args[1]
    msg = await message.answer(f"🔎 Сканирую базу сайтов для <b>{username}</b>... Это займет до 20 секунд.")
    result = await check_username_maigret(username)
    await msg.edit_text(result)

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())