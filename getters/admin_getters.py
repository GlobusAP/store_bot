from aiogram import Bot
from aiogram.types import User
from aiogram_dialog import DialogManager


async def category_or_item_getter(dialog_manager: DialogManager, bot: Bot, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    category = dialog_manager.dialog_data.get('category')
    item = dialog_manager.dialog_data.get('item_name')
    return {'category': category, 'item': item}


async def save_item_getter(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    return dialog_manager.dialog_data
