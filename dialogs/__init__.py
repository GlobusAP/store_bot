from aiogram import Router

from .dialog import start_dialog, catalog_dialog, basket_dialog
from .admin_dialog import admin_dialog, admin_del_dialog

dialogs_router = Router()

dialogs_router.include_routers(
    start_dialog,
    catalog_dialog,
    basket_dialog,
    admin_dialog,
    admin_del_dialog
)

