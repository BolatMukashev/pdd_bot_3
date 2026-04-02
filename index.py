from bot_logic import TgHandler
import asyncio


def handler(event: dict, context: str):
    # запускаем ассинхронную функцию, которая займётся обработкой полученного сообщения
    result = asyncio.get_event_loop().run_until_complete(TgHandler().cloud_run(event))
    return {
        'statusCode': 200,
        'body': result
    }