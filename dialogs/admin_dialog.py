from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, SwitchTo, Row, Next

from dialogs.checks import category_check, num_check
from getters.admin_getters import category_or_item_getter, save_item_getter
from handlers.admin_handler import (add_category, save_category_cmd, add_item, error_item, save_item_cmd,
                                    del_category, del_item, back_button)
from states.states import AdminSG, AdminDelSG

admin_dialog = Dialog(
    Window(
        Const('Введите название категории:'),
        TextInput(
            id='category',
            type_factory=category_check,
            on_success=add_category,
        ),
        Cancel(Const('◀️ Назад'), id='b_back'),
        state=AdminSG.category,
    ),
    Window(
        Format('Название новой категории:\n{category}\nСохранить?'),
        Button(Const('Сохранить?'), id='save_category', on_click=save_category_cmd),
        Back(Const('◀️ Назад'), id='b_back'),
        getter=category_or_item_getter,
        state=AdminSG.save_category
    ),
    Window(
        Const('Введите название товара:'),
        Format('Старое название: {item_name}', when='change_item'),
        TextInput(
            id='item_name',
            type_factory=category_check,
            on_success=add_item,
        ),
        Button(Const('◀️ Назад'), id='b_back', on_click=back_button),
        Next(Const('Пропустить'), id='b_next', when='change_item'),
        getter=save_item_getter,
        state=AdminSG.add_item
    ),
    Window(
        Const('Введите описание товара:'),
        Format('Старое описание:\n{item_description}', when='change_item'),
        TextInput(
            id='item_description',
            type_factory=category_check,
            on_success=add_item,
        ),
        Back(Const('◀️ Назад'), id='b_back'),
        Next(Const('Пропустить'), id='b_next', when='change_item'),
        getter=save_item_getter,
        state=AdminSG.item_description
    ),
    Window(
        Const('Введите стоимость товара:'),
        Format('Старая цена:\n{item_price}', when='change_item'),
        TextInput(
            id='item_price',
            type_factory=num_check,
            on_success=add_item,
            on_error=error_item
        ),
        Back(Const('◀️ Назад'), id='b_back'),
        Next(Const('Пропустить'), id='b_next', when='change_item'),
        getter=save_item_getter,
        state=AdminSG.item_price
    ),
    Window(
        Const('Введите количество товара:'),
        Format('Старое количество:\n{item_amount}', when='change_item'),
        TextInput(
            id='item_amount',
            type_factory=num_check,
            on_success=add_item,
            on_error=error_item
        ),
        Back(Const('◀️ Назад'), id='b_back'),
        Next(Const('Пропустить'), id='b_next', when='change_item'),
        getter=save_item_getter,
        state=AdminSG.item_amount
    ),
    Window(
        Format('В категории: {category}\n'
               'Название товара: {item_name}\n'
               'Описание: {item_description}\n'
               'Цена: {item_price}\n'
               'Количество: {item_amount}\n'
               'Сохранить?'),
        Button(Const('Сохранить?'), id='save_category', on_click=save_item_cmd),
        SwitchTo(Const('◀️ Назад'), id='b_back', state=AdminSG.add_item),
        getter=save_item_getter,
        state=AdminSG.save_item
    )
)

admin_del_dialog = Dialog(
    Window(
        Format('Удлить категорию {category}?'),
        Row(
            Button(Const('Да'), id='b_yes', on_click=del_category),
            Cancel(Const('Нет'))
        ),
        getter=category_or_item_getter,
        state=AdminDelSG.category_del
    ),
    Window(
        Format('Удалить товар {item}?'),
        Row(
            Button(Const('Да'), id='b_yes', on_click=del_item),
            Cancel(Const('Нет'))
        ),
        getter=category_or_item_getter,
        state=AdminDelSG.item_del
    )
)
