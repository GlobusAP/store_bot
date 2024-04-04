import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.config import Config, load_config
from handlers import handlers_router
from dialogs import dialogs_router
from middlewares.db import DataBaseSession
from database.models import async_main

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config: Config = load_config()
    engine = create_async_engine(config.db.url_db)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    await async_main(engine)

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    bot.my_admins_list = []

    dp.update.middleware(DataBaseSession(session_pool=async_session))

    dp.include_routers(handlers_router, dialogs_router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
