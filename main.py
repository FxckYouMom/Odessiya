import requests
from bs4 import BeautifulSoup
import re
import time
from fake_useragent import UserAgent
import json

def send_telegram_message(text):
    bot_token = '7670785514:AAEFcjugKWjzYuspIx2yJ7Ue9m1SwfOPz5o'
    chat_id = '-1002452439427'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    response = requests.get(url, params=payload)
    try:
        pass  # Ignoring response for now
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

def send_super_list_telegram(super_list, processed_ids):
    for item in super_list:
        # If the item ID has already been processed, skip it
        if item['id'] in processed_ids:
            continue

        # Encode the market name for the URL
        market_name_encoded = item['market_name'].replace(' ', '%20').replace('(', '%28').replace(')', '%29')
        market_url = f"https://steamcommunity.com/market/listings/730/{market_name_encoded}"

        # Create a numbered list of stickers
        stickers_message = "\n".join(
            [f"{i + 1}. [{name}]({url})" for i, (name, url) in enumerate(zip(item['sticker_names'], item['stickers']))]
        ) if item['stickers'] else 'No stickers'

        message = (
            f"*Предмет*: [{item['market_name']}]({market_url})\n\n"
            f"*Стікери:*\n{stickers_message}\n\n"
            f"*ID*: {item['id']}\n"
            f"*Тип*: {item['type']}\n\n"
            f"[Швидка Покупка]({market_url})"
        )

        send_telegram_message(message)
        processed_ids.add(item['id'])  # Add the ID to the processed list
        time.sleep(2)  # To prevent spamming requests

def main():
    ua = UserAgent()
    urls = [
        # Add your URLs here...
    ]
    
    specific_stickers = [ 
        "Sticker: (gold)", "Sticker:  (Lenticular)",
        "| Cologne 2014", "| Katowice 2015", "| DreamHack 2014", 
        "| Cluj-Napoca 2015", "| MLG Columbus 2016", 
        "| Cologne 2016", "| Krakow 2017", "| Atlanta 2017", 
        "| London 2018", "| Katowice 2019"
    ]  

    super_list = []
    processed_ids = set()  # Set to track processed item IDs

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

        # Check if the processed_ids set exceeds 1000 items, then clear it
        if len(processed_ids) > 1000:
            processed_ids.clear()

    send_super_list_telegram(super_list, processed_ids)


send_telegram_message("b")
if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
