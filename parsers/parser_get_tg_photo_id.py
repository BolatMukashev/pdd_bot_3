from pathlib import Path
import requests
import sys
import os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def get_photo_id(file_path, bot_token, admin_id):
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        print(f"Файл не найден: {path.name}")
        return None

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    with path.open("rb") as f:
        response = requests.post(
            url,
            files={"photo": f},
            data={"chat_id": admin_id}
        )

    result = response.json()

    if not result.get("ok"):
        print("Ошибка Telegram:", result)
        return None

    file_id = result["result"]["photo"][-1]["file_id"]

    sleep(0.6) # чтобы избежать превышения лимита запросов к Telegram API

    return file_id


if __name__ == "__main__":
    file_path = r"C:\Users\Astana\Desktop\Client\пдд\9.jpg"
    file_id = get_photo_id(file_path)
    print(file_id)