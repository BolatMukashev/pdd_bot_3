from dotenv import dotenv_values
import os

config = dotenv_values(".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN") or config.get('BOT_TOKEN')
TEST_BOT_TOKEN = os.environ.get("TEST_BOT_TOKEN") or config.get('TEST_BOT_TOKEN')

TEST_CHAT_ID = os.environ.get("TEST_CHAT_ID") or config.get('TEST_CHAT_ID')

ADMIN_ID = os.environ.get("ADMIN_ID") or config.get('ADMIN_ID')

