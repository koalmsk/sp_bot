import asyncio
import logging
import sys
from aiogram.methods import DeleteWebhook
import bot_initer.bot_init as bot_init
from aiogram.fsm.storage.memory import MemoryStorage
from routers import routers
from aiogram import Dispatcher
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    await bot_init.bot(DeleteWebhook(drop_pending_updates=True))

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers)
    await dp.start_polling(bot_init.bot)


if __name__ == "__main__":
    asyncio.run(main())
