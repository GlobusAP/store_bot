from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from database import requests as rq


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        getter_data = {'username': event_from_user.username or event_from_user.first_name or 'Stranger',
                       'first_show': True}
        dialog_manager.start_data.clear()
    else:
        getter_data = {'first_show': False}
    return getter_data


async def catalog_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    print(dialog_manager.current_stack())
    if dialog_manager.start_data:
        admin = dialog_manager.start_data.get('admin')
        dialog_manager.start_data.clear()
    else:
        admin = dialog_manager.dialog_data.get('admin')
    dialog_manager.dialog_data.update(admin=admin)
    all_categories = await rq.get_categories(session)
    categories = []
    for category in all_categories:
        categories.append((category.name, category.id))
    return {'categories': categories, 'admin': admin}


async def items_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    all_items = await rq.get_category_item(session, dialog_manager.dialog_data.get('category_id'))
    admin = dialog_manager.dialog_data.get('admin')
    category = dialog_manager.dialog_data.get('category')
    items = []
    for item in all_items:
        if int(item.amount) > 0 and not admin:
            items.append((item.name, item.id, item.amount))
        if admin:
            items.append((item.name, item.id, item.amount))
    return {'items': items, 'y_items': True, 'admin': admin, 'category': category}


async def item_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    admin = dialog_manager.dialog_data.get('admin')
    item = await rq.get_item(session, dialog_manager.dialog_data.get('item_id'))
    dialog_manager.dialog_data.update(item_amount=item.amount, item_name=item.name,
                                      item_description=item.description, item_price=item.price)
    return {'name': item.name, 'description': item.description, 'price': item.price, 'amount': item.amount,
            'admin': admin}


async def basket_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    basket_list = await rq.get_basket(session, int(dialog_manager.start_data.get('tg_id')))
    baskets = []
    price = 0
    amount = 0
    for basket_item in basket_list:
        item = await rq.get_item(session, basket_item.item)
        baskets.append((item.name, item.id, item.price, basket_item.id))

        price += item.price
        amount += 1
    return {'baskets': baskets, 'price': price, 'amount': amount}
