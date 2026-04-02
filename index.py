from main import dp, bot
import asyncio
import json
from aiogram.types import Update

def handler(event: dict, context):
    body = json.loads(event["body"])
    result = asyncio.get_event_loop().run_until_complete(process_update(body))
    return {
        "statusCode": 200,
        "body": "ok"
    }

async def process_update(body: dict):
    update = Update.model_validate(body)
    await dp.feed_update(bot, update)