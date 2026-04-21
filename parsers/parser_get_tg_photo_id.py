from pathlib import Path
import requests
import sys
import os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import TEST_BOT_TOKEN, ADMIN_ID


def get_photo_id(file_path):
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        print(f"Файл не найден: {path}")
        return None

    url = f"https://api.telegram.org/bot{TEST_BOT_TOKEN}/sendPhoto"

    with path.open("rb") as f:
        response = requests.post(
            url,
            files={"photo": f},
            data={"chat_id": ADMIN_ID}
        )

    result = response.json()

    if not result.get("ok"):
        print("Ошибка Telegram:", result)
        return None

    file_id = result["result"]["photo"][-1]["file_id"]

    sleep(1) # чтобы избежать превышения лимита запросов к Telegram API

    return file_id


if __name__ == "__main__":
    file_path = r"C:\Users\Astana\Desktop\Client\пдд\9.jpg"
    file_id = get_photo_id(file_path)
    print(file_id)