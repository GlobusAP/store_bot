from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession


from states.states import StartSG, CatalogSG, BasketSG, AdminSG, AdminDelSG
from database import requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager, session: AsyncSession):
    await rq.set_user(session, message.from_user.id)
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, data={'first_show': True})


async def to_catalog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.current_stack().intents = dialog_manager.current_stack().intents[:1]
    await dialog_manager.start(state=CatalogSG.open_catalog)


async def category_selection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, category_id: str):
    category, category_id = category_id.split('_')
    dialog_manager.dialog_data.update(category=category, category_id=int(category_id))
    await dialog_manager.next()


async def item_selection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: int):
    dialog_manager.dialog_data.update(item_id=int(item_id))
    await dialog_manager.next()


async def to_basket(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    item_id = dialog_manager.dialog_data.get('item_id')
    item = await rq.get_item(session, item_id)
    item_amount = item.amount
    if item_amount > 0:
        await rq.set_basket(session, int(callback.from_user.id), item_id)
        await callback.answer('Товар добавлен в корзину', show_alert=True)
        await rq.update_item(session, item_id, item_amount - 1)
    else:
        await callback.answer('Товар закончился', show_alert=True)
    await dialog_manager.back()


async def get_basket_cmd(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=BasketSG.basket, data={'tg_id': int(callback.from_user.id)})


async def basket_item_cmd(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, items_id: str):
    item_id, basket_item_id = items_id.split('_')
    dialog_manager.dialog_data.update(item_id=int(item_id), basket_item_id=int(basket_item_id))
    await dialog_manager.next()


async def delete_from_basket(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    basket_item_id = dialog_manager.dialog_data.get('basket_item_id')
    item_id = dialog_manager.dialog_data.get('item_id')
    item_amount = dialog_manager.dialog_data.get('item_amount')
    await rq.update_item(session, item_id, int(item_amount) + 1)
    await rq.delete_basket(session, callback.from_user.id, item_id, basket_item_id)
    await callback.answer('Товар удален из корзины')
    await dialog_manager.back()


async def to_add_item(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if button.widget_id == 'change_item':
        dialog_manager.dialog_data['change_item'] = True
    await dialog_manager.start(state=AdminSG.add_item, data=dialog_manager.dialog_data)


async def to_del_category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=AdminDelSG.category_del, data=dialog_manager.dialog_data)


async def to_del_item(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=AdminDelSG.item_del, data=dialog_manager.dialog_data)
