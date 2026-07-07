"""Главный файл для запуска бота"""

import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.db.database import init_db
from app.bot.handlers import start_router, feedback_router

# Загружаем переменные окружения
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция"""
    
    # Инициализируем БД
    await init_db()
    logger.info("✅ Database initialized")
    
    # Получаем токен
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN not found in .env file")
    
    # Создаем бота и диспетчер
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(feedback_router)
    
    logger.info("✅ Bot started")
    logger.info("🤖 Polling...")
    
    try:
        # Запускаем polling
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
