import requests
from bs4 import BeautifulSoup
import re
import time
from fake_useragent import UserAgent
import json

# Global list to track sent item IDs
sent_ids = []

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

def fetch_sticker_price(sticker_name):
    # Encode the sticker name for the URL
    market_name_encoded = sticker_name.replace(' ', '%20').replace('|', '%7C')
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=18&market_hash_name=Sticker%20%7C%20{market_name_encoded}"
    
    try:
        response = requests.get(url).json()
        if response.get('success'):
            return response.get('lowest_price', 'N/A')  # Return 'N/A' if no price is available
    except Exception as e:
        #print(f"Error fetching price for {sticker_name}: {e}")
        pass
    
    return 'N/A'

def extract_sticker_info(item):
    stickers = []
    sticker_names = []
    sticker_prices = []
    for desc in item.get("descriptions", []):
        if 'sticker_info' in desc.get("value", ""):
            sticker_urls = re.findall(r'src="([^"]+)"', desc["value"])
            sticker_names = re.findall(r'Sticker:\s*([^<]+)', desc["value"])
            if sticker_names:
                stickers = sticker_urls
                sticker_names = sticker_names[0].split(', ')
                
                # Fetch prices for each sticker
                sticker_prices = [fetch_sticker_price(name) for name in sticker_names]
                
    return stickers, sticker_names, sticker_prices

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
                        "sticker_names": [],
                        "sticker_prices": []
                    }
                    item_info["stickers"], item_info["sticker_names"], item_info["sticker_prices"] = extract_sticker_info(item)
                    extracted_data.append(item_info)
    return extracted_data

def send_super_list_telegram(super_list):
    global sent_ids  # Access the global variable
    for item in super_list:
        if item['id'] in sent_ids:
            continue  # Skip sending the message if the item has already been processed

        # Encode the market name for the URL
        market_name_encoded = item['market_name'].replace(' ', '%20').replace('(', '%28').replace(')', '%29')
        market_url = f"https://steamcommunity.com/market/listings/730/{market_name_encoded}"

        # Create a numbered list of stickers with prices
        stickers_message = "\n".join(
            [f"{i + 1}. [{name}]({url}) - {price}" for i, (name, url, price) in enumerate(zip(item['sticker_names'], item['stickers'], item['sticker_prices']))]
        ) if item['stickers'] else 'No stickers'

        message = (
            f"*Предмет*: [{item['market_name']}]({market_url})\n\n"
            f"*Стікери:*\n{stickers_message}\n\n"
            f"*ID*: {item['id']}\n"
            f"*Тип*: {item['type']}\n\n"
            f"[Швидка Покупка]({market_url})"
        )

        send_telegram_message(message)

        # Add the item ID to the sent list
        sent_ids.append(item['id'])

        # Clear the list if it grows too large
        if len(sent_ids) > 1000:
            sent_ids.clear()

        time.sleep(2)  # To prevent spamming requests

def main():
    ua = UserAgent()

    urls = [
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Check%20Engine%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Check%20Engine%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Check%20Engine%20%28Factory%20New%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Torque%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Cyrex%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Cyrex%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Blood%20Tiger%20%28Minimal%20Wear%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Blood%20Tiger%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Candy%20Apple%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Candy%20Apple%20%28Minimal%20Wear%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/P250%20%7C%20Metallic%20DDPAT%20%28Factory%20New%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/P250%20%7C%20Metallic%20DDPAT%20%28Minimal%20Wear%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/Galil%20AR%20%7C%20Tuxedo%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/Galil%20AR%20%7C%20Eco%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/Galil%20AR%20%7C%20Eco%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Emerald%20Pinstripe%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Emerald%20Pinstripe%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Safety%20Net%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Safety%20Net%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Nitro%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Nitro%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Nitro%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Converter%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Converter%20%28Well-Worn%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Converter%20%28Minimal%20Wear%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Evil%20Daimyo%20%28Battle-Scarred%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Evil%20Daimyo%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Urban%20DDPAT%20%28Field-Tested%29?filter=Sticker%3A",
    "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Urban%20DDPAT%20%28Minimal%20Wear%29?filter=Sticker%3A"
]
    
    specific_stickers = [ 
        "Sticker: (gold)", "Sticker:  (Lenticular)",
        "| Cologne 2014", "| Katowice 2015", "| DreamHack 2014", 
        "| Cluj-Napoca 2015", "| MLG Columbus 2016", 
        "| Cologne 2016", "| Krakow 2017", "| Atlanta 2017", 
        "| London 2018", "| Katowice 2019"
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

send_telegram_message("hi")
if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)  # Increase the delay to avoid too frequent scraping
