from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Button, Group, Select, Cancel, Back, ScrollingGroup, Start)

from getters.getter import catalog_getter, items_getter, item_getter, basket_getter, username_getter
from handlers.start_handler import (
    category_selection,
    item_selection,
    to_basket,
    get_basket_cmd,
    basket_item_cmd,
    delete_from_basket,
    to_catalog,
    to_add_item,
    to_del_category,
    to_del_item)
from states.states import StartSG, CatalogSG, BasketSG, AdminSG


def when_not(key: str):
    def f(data, whenable, manager):
        return not data.get(key)
    return f


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n', when='first_show'),
        Const('<b>Вы вошли в интернет магазин!</b>'),
        Start(Const('🗂 Каталог'), id='b_catalog', state=CatalogSG.open_catalog),
        getter=username_getter,
        state=StartSG.start
    ),
)

catalog_dialog = Dialog(
    Window(
        Const(text='Выберите категорию:'),
        Group(
            Select(
                Format('{item[0]}'),
                id='category',
                item_id_getter=lambda x: f'{x[0]}_{x[1]}',
                items='categories',
                on_click=category_selection,
            ),
            width=2
        ),
        Cancel(Const('В начало'), id='to_start', when=when_not('admin')),
        Button(Const('🗑 Корзина'), id='basket', on_click=get_basket_cmd, when=when_not('admin')),
        Start(Const('Добавить категорию'), id='is_admin', when='admin', state=AdminSG.category),
        getter=catalog_getter,
        state=CatalogSG.open_catalog
    ),
    Window(
        Const(text='Выберете товар:', when='items'),
        Format(text='В категории {category} товар отсутствует', when=when_not('items')),
        ScrollingGroup(
            Select(
                Format('{item[0]}  ({item[2]} шт.)'),
                id='items',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=item_selection,
            ),
            id='items_id',
            width=1, height=5,
            hide_on_single_page=True
        ),
        Back(Const('◀️ Назад'), id='b_back'),
        Button(Format('Удалить категорию {category}'), id='del_category', when='admin', on_click=to_del_category),
        Button(Format('Добавить товар в категорию {category}'), id='add_item', when='admin', on_click=to_add_item),
        Button(Const('🗑 Корзина'), id='basket', on_click=get_basket_cmd, when=when_not('admin')),
        getter=items_getter,
        state=CatalogSG.items,
    ),
    Window(
        Format('{name}\n{description}\nЦена: {price}$\nВ наличии: {amount}'),
        Button(Const('В корзину'), id='b_basket', on_click=to_basket, when=when_not('admin')),
        Back(Const('◀️ Назад'), id='b_back'),
        Button(Const('🗑\nКорзина'), id='basket', on_click=get_basket_cmd, when=when_not('admin')),
        Button(Format('Изменить'), id='change_item', when='admin', on_click=to_add_item),
        Button(Format('Удалить'), id='del_item', when='admin', on_click=to_del_item),
        getter=item_getter,
        state=CatalogSG.item
    )
)

basket_dialog = Dialog(
    Window(
        Const('🗑 Корзина:', when='baskets'),
        Const('Корзина пуста', when=when_not('baskets')),
        ScrollingGroup(
            Select(
                Format('{item[0]}, Цена: {item[2]}$'),
                id='basket_item',
                item_id_getter=lambda x: f'{x[1]}_{x[3]}',
                items='baskets',
                on_click=basket_item_cmd
            ),
            id='baskets_id',
            width=1, height=5,
            hide_on_single_page=True
        ),

        Format('Заказов {amount} на сумму {price}$', when='baskets'),
        # исправить Cancel!
        Cancel(Const('◀️ Назад'), id='b_back'),
        Button(Const('⬆️ В каталог'), id='to_categories', on_click=to_catalog),
        getter=basket_getter,
        state=BasketSG.basket
    ),
    Window(
        Const('🗑 Корзина:'),
        Format('{name}\n{description}\nЦена: {price}$\n'),
        Button(Const('Удалить товар из корзины'), id='del_item_basket', on_click=delete_from_basket),
        Back(Const('◀️ Назад'), id='b_back'),
        getter=item_getter,
        state=BasketSG.basket_item,
    )
)
