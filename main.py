import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Получаем токен из переменных окружения (безопасность!)
BOT_TOKEN = os.getenv("ENV_BOT_TOKEN")
# Порт, который выдаёт хостинг (по умолчанию 8080)
PORT = int(os.getenv("PORT", 8080))

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Хэндлеры команд ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("tac1ical OSINT на связи.\nЯ готов к работе.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - Приветствие\n/help - Помощь\n/ip - Скоро...")

# --- Настройка Webhook ---

async def on_startup(bot: Bot):
    # Ссылка на твой хостинг (замени на свой URL на Render)
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(f"{webhook_url}/webhook")
        print(f"Webhook установлен: {webhook_url}/webhook")

def main():
    app = web.Application()

    # Регистрация вебхука
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, dp, bot=bot)

    # Запуск сервера
    web.run_app(app, host="0.0.0.0", port=PORT, on_startup=on_startup)

if __name__ == "__main__":
    main()