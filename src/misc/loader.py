# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os
import sqlite3
import time

from src.misc.config import *


def get_logger():
    logging.basicConfig(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s:%(filename)s:%(lineno)d | %(message)s')
    handler = logging.FileHandler(
        os.path.join(
            os.getcwd(),
            'logging',
            f'{time.strftime("%Y_%m_%d-%H_%M_%S", time.localtime())}.log'
        ),
        mode='w',
        encoding='utf-8'
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    apscheduler_logger = logging.getLogger('apscheduler')
    apscheduler_logger.setLevel(logging.DEBUG)
    apscheduler_logger.addHandler(handler)
    
    return root_logger



bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = get_logger()

scheduler = AsyncIOScheduler()
scheduler.start()

connection = sqlite3.connect('database.db')
cursor = connection.cursor()