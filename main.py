# - *- coding: utf- 8 - *-
from aiogram import executor, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
import asyncio
import sqlite3

from src.handlers import dp
from src.misc.config import UPDATE_TIME
from src.misc.loader import bot, logger,  scheduler, connection, cursor
from src.utils.bot_service import admins_mailing, send_notifications
from src.utils.tools import get_last_task_id


async def set_commands():
    # Команды для пользователей
    user_commands = [
        BotCommand("start", "📣 Главное меню"),
    ]
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())


async def scheduler_start():
    scheduler.add_job(send_notifications, 'interval', minutes=UPDATE_TIME)


async def set_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Key (
    id INTEGER PRIMARY KEY DEFAULT 0,
    task_id INTEGER
    )
    ''')
    connection.commit()
    
    last_task_id = await get_last_task_id()
    try:
        cursor.execute("INSERT INTO Key (id, task_id) VALUES (0, ?)", (last_task_id,))
    except sqlite3.IntegrityError:
        cursor.execute("UPDATE Key SET task_id = ? WHERE id = 0", (last_task_id,))
    connection.commit()


async def on_startup(dp: Dispatcher):
    logger.info("Бот запущен")
    await set_commands()
    await set_db()
    
    await admins_mailing("✅ Бот запущен")
    
    asyncio.create_task(scheduler_start())


async def on_shutdown(dp: Dispatcher):
    logger.info("Остановка бота..")
    connection.close()
    await admins_mailing("❌ Бот остановлен")
    logger.info("Бот остановлен")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
