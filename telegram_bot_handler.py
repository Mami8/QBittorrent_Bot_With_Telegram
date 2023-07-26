import requests
import argparse

"""
Kullanmak için gerekli bilgileri şu sirayla 
"bot_info.txt" 
ismindeki bir metin belgesine kaydedin:

-API key
-Chat ID

+-+ API key'i eğer Bot Father kullandiysaniz botu oluştururken göreceksiniz.

+-+ Chat ID'nizi almak için şu kodu uygun yerleri doldurup çaliştirim:
~~~
import requests
TOKEN = "YOUR TELEGRAM BOT TOKEN"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
print(requests.get(url).json())
~~~
Çikti içerisinde chat ID'niz bulunmakta.

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

uçbirim (terminal) üzerinden _python.exe /kodun/bulunduğu/yol/telegram_bot_handler.py "(mesajiniz)"_ şeklinde kullanablirsiniz
"""


with open("D:/Code/Piton/bot_info.txt", "r") as f:
    info = f.readlines()
    TOKEN = info[0].strip()
    chat_id = info[1].strip()


def send_message(message: str):
    """Mesaj gönderir"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())


def main():
    parser = argparse.ArgumentParser(description="Telegram mesaj gönderme scripti")
    parser.add_argument("message", metavar="N", type=str, help="Message to send")

    args = parser.parse_args()

    if args.message:
        send_message(args.message)


if __name__ == "__main__":
    main()
