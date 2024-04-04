from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


# user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await bot.delete_message(chat_id, message.message_id)


@user_group_router.chat_member()
async def status_check(event: ChatMemberUpdated, session: AsyncSession, bot: Bot):
    if event.old_chat_member.user.id in bot.my_admins_list and event.old_chat_member.status.ADMINISTRATOR \
            and event.new_chat_member.status.MEMBER:
        print(event.from_user.id)
        bot.my_admins_list.remove(event.old_chat_member.user.id)
    print(bot.my_admins_list)
