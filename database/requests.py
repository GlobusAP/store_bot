from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Category, Item, Basket
from sqlalchemy import select, update, delete


async def set_user(session: AsyncSession, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()


async def get_categories(session: AsyncSession):
    return await session.scalars(select(Category))


async def get_category_item(session: AsyncSession, category_id):
    return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(session: AsyncSession, item_id):
    return await session.scalar(select(Item).where(Item.id == item_id))


async def set_basket(session: AsyncSession, tg_id, item_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    session.add(Basket(user=user.id, item=item_id))
    await session.commit()


async def update_item(session: AsyncSession, item_id, amount):
    query = update(Item).where(Item.id == item_id).values(amount=amount)
    await session.execute(query)
    await session.commit()


async def get_basket(session: AsyncSession, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    return await session.scalars(select(Basket).where(Basket.user == user.id))


async def delete_basket(session: AsyncSession, tg_id, item_id, basket_item_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    query = delete(Basket).where(Basket.user == user.id,
                                 Basket.item == item_id, Basket.id == basket_item_id)
    await session.execute(query)
    await session.commit()


async def save_category(session: AsyncSession, category):
    obj = Category(name=category)
    session.add(obj)
    await session.commit()


async def save_item(session: AsyncSession, data):
    obj = Item(
        name=data['item_name'],
        description=data['item_description'],
        price=data['item_price'],
        category=data['category_id'],
        amount=data['item_amount']
    )
    session.add(obj)
    await session.commit()


async def update_item_values(session: AsyncSession, data):
    item_id = data.get('item_id')
    query = update(Item).where(Item.id == item_id).values(
        name=data['item_name'],
        description=data['item_description'],
        price=data['item_price'],
        category=data['category_id'],
        amount=data['item_amount']
    )
    await session.execute(query)
    await session.commit()


async def delete_category(session: AsyncSession, category_id):
    query = delete(Category).where(Category.id == category_id)
    await session.execute(query)
    await session.commit()


async def delete_item(session: AsyncSession, item_id):
    query = delete(Item).where(Item.id == item_id)
    await session.execute(query)
    await session.commit()
