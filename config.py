from dotenv import dotenv_values
import os

config = dotenv_values(".env")

BOT_API_KEY = os.environ.get("BOT_API_KEY") or config.get('BOT_API_KEY')

