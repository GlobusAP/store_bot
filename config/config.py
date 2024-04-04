from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class DB:
    name: str
    user: str
    password: str
    port: int
    host: str

    def __post_init__(self):
        self.url_db = f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


# @dataclass
# class DB:
#     name: str
#
#     def __post_init__(self):
#         self.url_db = f'sqlite+aiosqlite:///{self.name}'


@dataclass
class Config:
    tg_bot: TgBot
    db: DB


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')),
        db=DB(
            name=env('POSTGRES_NAME'),
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            port=env('POSTGRES_PORT'),
            host=env('POSTGRES_HOST')
        ))


# def load_config(path: str | None = None) -> Config:
#     env = Env()
#     env.read_env(path=path)
#     return Config(
#         tg_bot=TgBot(
#             token=env('BOT_TOKEN')),
#         db=DB(
#             name=env('SQLITE_NAME')))
