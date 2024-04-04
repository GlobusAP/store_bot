from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()


class CatalogSG(StatesGroup):
    open_catalog = State()
    items = State()
    item = State()
    basket = State()
    basket_item = State()


class BasketSG(StatesGroup):
    basket = State()
    basket_item = State()


class AdminSG(StatesGroup):
    category = State()
    save_category = State()
    add_item = State()
    item_description = State()
    item_price = State()
    item_amount = State()
    save_item = State()


class AdminDelSG(StatesGroup):
    category_del = State()
    item_del = State()
