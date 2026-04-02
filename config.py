from dotenv import dotenv_values
import os

config = dotenv_values(".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN") or config.get('BOT_TOKEN')


FUNCTION_ID = os.environ.get("FUNCTION_ID") or config.get('FUNCTION_ID')
FUNCTION_URL = f"https://functions.yandexcloud.net/{FUNCTION_ID}"
