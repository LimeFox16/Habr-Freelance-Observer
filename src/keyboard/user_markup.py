from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


link_to_github = InlineKeyboardButton('GitHub', url='https://github.com/LimeFox16/Habr-Freelance-Observer')
link_to_github_keyboard = InlineKeyboardMarkup().add(link_to_github)


async def new_task_keyboard(url: str = '_') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Ссылка', url=url)
    )
    return keyboard