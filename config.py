from dotenv import dotenv_values
import os

config = dotenv_values(".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN") or config.get('BOT_TOKEN')
TEST_BOT_TOKEN = os.environ.get("TEST_BOT_TOKEN") or config.get('TEST_BOT_TOKEN')

TEST_CHAT_ID = os.environ.get("TEST_CHAT_ID") or config.get('TEST_CHAT_ID')

ADMIN_ID = int(os.environ.get("ADMIN_ID") or config.get('ADMIN_ID'))

YDB_TOKEN = os.environ.get("YDB_TOKEN") or config.get('YDB_TOKEN')
YDB_ENDPOINT = os.environ.get("YDB_ENDPOINT") or config.get('YDB_ENDPOINT')
YDB_PATH = os.environ.get("YDB_PATH") or config.get('YDB_PATH')

AMOUNT = int(os.environ.get("AMOUNT") or config.get('AMOUNT'))