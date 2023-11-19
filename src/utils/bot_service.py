from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from src.keyboard.user_markup import new_task_keyboard
from src.misc.config import ADMINS_IDS, MAIN_ADMIN_ID
from src.misc.loader import bot, connection, cursor
from src.text.user_text import new_task
from src.utils.tools import get_unread_tasks, get_last_task_id


async def admins_mailing(text: str = 'Hello', **kwargs):
    all_admins = [MAIN_ADMIN_ID]
    all_admins.extend(ADMINS_IDS)

    for admin_id in all_admins:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
                **kwargs
            )
        except (BotBlocked, ChatNotFound):
            continue


async def send_notifications():
    data = await get_unread_tasks()
    
    last_task_id = await get_last_task_id()
    cursor.execute("UPDATE Key SET task_id = ? WHERE id = 0", (last_task_id,))
    connection.commit()
    
    for task in data:
        await admins_mailing(
            text=new_task.format(
                title=task.get('title'),
                price=task.get('price'),
                tags=" ".join(task.get('tags')),
                urgent='Срочный заказ' if task.get('urgent') else '',
            ),
            reply_markup=await new_task_keyboard(
                url=task.get('url')
            )
)
