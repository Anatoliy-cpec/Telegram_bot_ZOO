import asyncio
import logging
import os
import json

from aiogram import Bot, Dispatcher, types

from antiflood import ThrotlingMiddleware
import my_commands, state_handlers, text_handlers, callback_handlers

# логи в консоль
logging.basicConfig(level=logging.INFO)


bot = Bot(os.environ.get('API_TOKEN'))
dp = Dispatcher()
# подключаю антиспам
dp.message.middleware(ThrotlingMiddleware())
# цепляю на диспатчер роутеры
dp.include_routers(my_commands.router, state_handlers.router, callback_handlers.router, text_handlers.router)

async def process_event(event):

    update = types.Update.model_validate(json.loads(event['body']), context={"bot": bot})
    await dp.feed_update(bot, update)

async def webhook(event, context):
    if event['httpMethod'] == 'POST':
        # Bot and dispatcher initialization
        # Объект бота


        await process_event(event)
        return {'statusCode': 200, 'body': 'ok'}

    return {'statusCode': 405}

async def main():
    # запускаю полинг
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())



