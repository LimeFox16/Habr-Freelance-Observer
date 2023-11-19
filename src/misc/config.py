from dotenv import load_dotenv
import os
from typing import List


if not load_dotenv():
    raise Exception("Невозможно прогрузить .env файл. Возможно, он находится не в той директории")

MAIN_ADMIN_ID: int = int(os.getenv("MAIN_ADMIN_ID"))
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMINS_IDS: List[int] = list(map(int, os.getenv("ADMINS_IDS").replace(',', '').split()))
UPDATE_TIME: int = int(os.getenv('UPDATE_TIME'))