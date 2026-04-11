import requests
from config import TEST_BOT_TOKEN, ADMIN_ID


def get_photo_id(file_path):
    url = f"https://api.telegram.org/bot{TEST_BOT_TOKEN}/sendPhoto"
    
    with open(file_path, "rb") as f:
        files = {"photo": f}

        data = {
            "chat_id": ADMIN_ID
        }

        response = requests.post(url, files=files, data=data)
    result = response.json()
    file_id = result['result']['photo'][-1]['file_id']
    return file_id

if __name__ == "__main__":
    file_path = r"C:\Users\Astana\Desktop\Client\пдд\4.jpg"
    file_id = get_photo_id(file_path)
    print(file_id)
    