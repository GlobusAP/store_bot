from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from database import requests as rq
from states.states import CatalogSG, StartSG, AdminSG
from filters.chat_types import ChatTypeFilter, IsAdmin

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())


@admin_router.message(Command(commands=['admin', 'user']))
async def cmd_start(message: Message, dialog_manager: DialogManager, session: AsyncSession):
    data = {'admin': True}
    if message.text == '/user':
        await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.start(state=CatalogSG.open_catalog, mode=StartMode.RESET_STACK, data=data,
                                   show_mode=ShowMode.DELETE_AND_SEND)


async def add_category(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data[widget.widget.widget_id] = text
    await dialog_manager.switch_to(state=AdminSG.save_category)


async def check_admin(callback: CallbackQuery, dialog_manager: DialogManager):
    if callback.from_user.id not in dialog_manager.event.bot.my_admins_list:
        await callback.message.answer('Вы больше не админ')
        await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
        return False
    return True


async def save_category_cmd(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if await check_admin(callback, dialog_manager):
        category = dialog_manager.dialog_data.get('category')
        session: AsyncSession = dialog_manager.middleware_data.get('session')
        await rq.save_category(session, category)
        await dialog_manager.done()


async def add_item(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str | int):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    item = widget.widget.widget_id
    dialog_manager.dialog_data[item] = text
    await dialog_manager.next()


async def error_item(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await message.answer(text='Должно быть число. Попробуй еще раз.')


async def save_item_cmd(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if await check_admin(callback, dialog_manager):
        data = dialog_manager.dialog_data
        dialog_manager.start_data.update(data)
        session: AsyncSession = dialog_manager.middleware_data.get('session')
        if data.get('change_item'):
            await rq.update_item_values(session, data)
            await callback.answer('Изменения внесены')
            dialog_manager.dialog_data['change_item'] = False
        else:
            await rq.save_item(session, data)
        await dialog_manager.done()


async def del_category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if await check_admin(callback, dialog_manager):
        session: AsyncSession = dialog_manager.middleware_data.get('session')
        category_id = dialog_manager.dialog_data.get('category_id')
        await rq.delete_category(session, category_id)
        dialog_manager.current_stack().intents = dialog_manager.current_stack().intents[:1]
        await dialog_manager.start(state=CatalogSG.open_catalog, data={'admin': True})


async def del_item(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if await check_admin(callback, dialog_manager):
        session: AsyncSession = dialog_manager.middleware_data.get('session')
        item_id = dialog_manager.dialog_data.get('item_id')
        category_id = dialog_manager.dialog_data.get('category_id')
        category = dialog_manager.dialog_data.get('category')
        await rq.delete_item(session, item_id)
        dialog_manager.current_stack().intents = dialog_manager.current_stack().intents[:1]
        await dialog_manager.start(state=CatalogSG.items,
                                   data={'admin': True, 'category_id': category_id, 'category': category})


async def back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['change_item'] = False
    dialog_manager.start_data.update(dialog_manager.dialog_data)
    await dialog_manager.done()
