import requests
from bs4 import BeautifulSoup
import re
import time
from fake_useragent import UserAgent
import json  # Added this import

def send_telegram_message(text):
    bot_token = '7595540941:AAFtpRyiXk3-1DH--QShk-5_9pFM5TUY84s'
    chat_id = '-4540675671'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    response = requests.get(url, params=payload)
    try:
       # print(response.json()) 
        pass 
    except ValueError:
        print("Error in response")

def fetch_page(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

def extract_g_rgAssets(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        if 'g_rgAssets' in script.text:
            match = re.search(r'g_rgAssets = (.*?);\r\n', script.text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
    return None

def extract_sticker_info(item):
    stickers = []
    sticker_names = []
    for desc in item.get("descriptions", []):
        if 'sticker_info' in desc.get("value", ""):
            sticker_urls = re.findall(r'src="([^"]+)"', desc["value"])
            sticker_names = re.findall(r'Sticker:\s*([^<]+)', desc["value"])
            if sticker_names:
                stickers = sticker_urls
                sticker_names = sticker_names[0].split(', ')
    return stickers, sticker_names

def extract_data(g_rgAssets):
    extracted_data = []
    if isinstance(g_rgAssets, dict):
        for appid, contexts in g_rgAssets.items():
            for contextid, items in contexts.items():
                for item_id, item in items.items():
                    item_info = {
                        "id": item_id,
                        "market_name": item.get("market_name", ""),
                        "type": item.get("type", ""),
                        "stickers": [],
                        "sticker_names": []
                    }
                    item_info["stickers"], item_info["sticker_names"] = extract_sticker_info(item)
                    extracted_data.append(item_info)
    return extracted_data

# Создаем глобальный список для хранения уже отправленных id
sent_ids = []  

def send_super_list_telegram(super_list):
    global sent_ids  # Используем глобальный список

    for item in super_list:
        # Проверка, был ли уже отправлен этот id
        if item['id'] in sent_ids:
            continue  # Пропускаем элемент, если id уже был отправлен

        # Encode the market name for the URL
        market_name_encoded = item['market_name'].replace(' ', '%20').replace('(', '%28').replace(')', '%29')
        market_url = f"https://steamcommunity.com/market/listings/730/{market_name_encoded}"

        # Создаем список стикеров для сообщения
        stickers_message = "\n".join(
            [f"{i + 1}. [{name}]({url})" for i, (name, url) in enumerate(zip(item['sticker_names'], item['stickers']))]
        ) if item['stickers'] else 'No stickers'

        # Формируем сообщение для Telegram
        message = (
            f"*Предмет*: [{item['market_name']}]({market_url})\n\n"
            f"*Стикери:*\n{stickers_message}\n\n"
            f"*ID*: {item['id']}\n"
            f"*Тип*: {item['type']}\n\n"
            f"[Швидка Покупка]({market_url})"
        )

        # Отправляем сообщение в Telegram
        send_telegram_message(message)

        # Добавляем id в глобальный список отправленных
        sent_ids.append(item['id'])

        time.sleep(2)  # Задержка, чтобы не спамить запросы

def main():
    ua = UserAgent()
    urls = [
        "https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Blue%20Fissure%20%28Field-Tested%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Blue%20Fissure%20%28Battle-Scarred%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/P250%20%7C%20Metallic%20DDPAT%20%28Factory%20New%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Emerald%20Pinstripe%20%28Battle-Scarred%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Emerald%20Pinstripe%20%28Field-Tested%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Torque%20%28Minimal%20Wear%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/AWP%20%7C%20Acheron%20%28Field-Tested%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/AWP%20%7C%20Acheron%20%28Minimal%20Wear%29?filter=Sticker%3A",
        "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Nitro%20%28Field-Tested%29?filter=Sticker%3A"
    ]

    specific_stickers = [ 
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
    ]  

    super_list = []

    for url in urls:
        headers = {
            'User-Agent': ua.random
        }
        time.sleep(1)
        page_content = fetch_page(url, headers)
        soup = BeautifulSoup(page_content, 'html.parser')
        
        g_rgAssets = extract_g_rgAssets(soup)
        if g_rgAssets:
            extracted_data = extract_data(g_rgAssets)

            for item in extracted_data:
                for sticker_name in item['sticker_names']:
                    if any(re.search(re.escape(sticker), sticker_name, re.IGNORECASE) for sticker in specific_stickers):
                        super_list.append(item)
                        break

    send_super_list_telegram(super_list)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
