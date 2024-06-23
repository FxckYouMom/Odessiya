import requests
import time

def send_telegram_message(text):
    bot_token = '6346370947:AAFpePtGV60tX2PEv0rV0RK45h_VZcybx94'
    chat_id = '-1001795323643'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
    
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    while True:
        send_telegram_message("hi")
        time.sleep(600)
