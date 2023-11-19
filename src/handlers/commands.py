from aiogram.types import Message

from src.misc.loader import dp, bot, logger
from src.keyboard.user_markup import link_to_github_keyboard

@dp.message_handler(state='*', commands = 'start')
async def cmd_start(message: Message):

    await bot.send_message(
        chat_id=message.from_user.id,
        text = 'Hello, World!',
        reply_markup=link_to_github_keyboard
    )