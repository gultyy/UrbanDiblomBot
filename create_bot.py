from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, InputFile
from asyncpg_lite import DatabaseManager
from decouple import config

#Admin list of pulsepoll_bot
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

db_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

async def set_commands():
    """

    :return:
    """
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='take_poll', description='Пройти опрос'),
                BotCommand(command='stats', description='Статистика')
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
