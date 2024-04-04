from aiogram import Router

from handlers.start_handler import router
from handlers.admin_handler import admin_router
from handlers.user_group import user_group_router

handlers_router = Router()

handlers_router.include_routers(router,
                                admin_router,
                                user_group_router)