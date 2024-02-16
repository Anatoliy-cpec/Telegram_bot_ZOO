import asyncio
import logging
import os
from aiogram import Bot, Dispatcher

from antiflood import ThrotlingMiddleware
import my_commands, state_handlers, text_handlers, callback_handlers

# логи в консоль
# logging.basicConfig(level=logging.INFO)

# ////////////////////////// /////////////////////////

async def main():
    # логи в файл
    log_path = 'Telegram_bot/tg_bot_2/files/log.log'
    logging.basicConfig(level=logging.INFO, filename=log_path, filemode="a", format="%(asctime)s %(levelname)s %(message)s")

    bot = Bot(os.environ.get('TOKEN'))
    dp = Dispatcher()
    # подключаю антиспам
    dp.message.middleware(ThrotlingMiddleware())
    # цепляю на диспатчер роутеры
    dp.include_routers(my_commands.router, state_handlers.router, callback_handlers.router, text_handlers.router)
    # запускаю полинг
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())

