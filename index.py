import json
from aiogram.types import Update
from main import bot, dp, logger


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