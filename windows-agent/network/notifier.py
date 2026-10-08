import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram credentials are not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(url, data=data)

    if response.ok:
        print("Telegram message sent successfully!")
        return True

    print(f"Telegram error: {response.text}")
    return False


def send_telegram_photo(photo_path, caption="Device Sentinel Login Alert"):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram credentials are not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"

    try:
        with open(photo_path, "rb") as photo:
            files = {
                "photo": photo
            }

            data = {
                "chat_id": chat_id,
                "caption": caption,
            }

            response = requests.post(
                url,
                data=data,
                files=files,
            )

        if response.ok:
            print("Telegram photo sent successfully!")
            return True

        print(f"Telegram photo error: {response.text}")
        return False

    except Exception as error:
        print(f"Photo sending error: {error}")
        return False


if __name__ == "__main__":
    send_telegram_message("Device Sentinel test message 🚨")