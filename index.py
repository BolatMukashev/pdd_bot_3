import json
from aiogram.types import Update
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import logging
from main import commands_router, text_router, payment_router, media_router


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(commands_router)
dp.include_router(text_router)
dp.include_router(payment_router)
dp.include_router(media_router)


async def handler_async(event, context):
    try:
        logger.info(f"EVENT: {event}")

        # --- MQ обработка ---
        for msg in event.get("messages", []):
            body_str = msg["details"]["message"]["body"]
            body = json.loads(body_str)

            update = Update.model_validate(body)
            await dp.feed_update(bot, update)
        # ---------------------

        return {
            "statusCode": 200,
            "body": "ok"
        }

    except Exception as e:
        logger.exception("Ошибка обработки апдейта")
        return {
            "statusCode": 200,
            "body": str(e)
        }


def handler(event, context):
    import asyncio
    return asyncio.run(handler_async(event, context))