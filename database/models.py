from typing import List

from sqlalchemy import BigInteger, String, ForeignKey, text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True)
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

    basket_rel: Mapped[List['Basket']] = relationship(back_populates='user_rel')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

    item_rel: Mapped[List['Item']] = relationship(back_populates='category_rel')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column()

    basket_rel: Mapped[List['Basket']] = relationship(back_populates='item_rel')
    category_rel: Mapped['Category'] = relationship(back_populates='item_rel')


class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)

    user_rel: Mapped['User'] = relationship(back_populates='basket_rel')
    item_rel: Mapped['Item'] = relationship(back_populates='basket_rel')


async def async_main(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
