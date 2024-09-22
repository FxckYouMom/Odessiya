import requests
import json
import time
import urllib.parse
import os
import logging
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the user agent generator
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Load sensitive info from environment variables
BOT_TOKEN= '7670785514:AAEFcjugKWjzYuspIx2yJ7Ue9m1SwfOPz5o'
CHAT_ID= '-1002452439427'

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    try:
        time.sleep(0.5)  # Simple rate limit to avoid flooding the API
        response = requests.get(url, params=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        logging.error(f"Failed to send message: {e}")

stickers = [
    "Titan Katowice 2015",
    "Titan Cologne 2014",
    "Cloud9 G2A Katowice 2015",
    "Natus Vincere Katowice 2015",
    "HellRaisers Katowice 2015",
    "Vox Eminor Katowice 2015",
    "Vox Eminor Cologne 2014",
    "Cloud9 DreamHack 2014",
    "Team Dignitas DreamHack 2014",
    "Fnatic DreamHack 2014",
    "Natus Vincere DreamHack 2014",
    "Virtus.Pro DreamHack 2014",
    "Ninjas in Pyjamas DreamHack 2014",
    "Titan Katowice 2015",
    "LGB eSports Katowice 2015",
    "Flipsid3 Tactics Katowice 2015",
    "Cloud9 G2A Katowice 2015",
    "Counter Logic Gaming Katowice 2015",
    "Keyd Stars Katowice 2015",
    "3DMAX Katowice 2015",
]


filtered_sticker_data = {}

# Load previous data
def load_previous_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def fetch_sticker_data(sticker_name, session, headers, cookies):
    payload = {
        'query': f'"{sticker_name}"',
        'start': '0',
        'count': '20',
        'search_descriptions': '1',
        'sort_column': 'price',
        'sort_dir': 'asc',
        'appid': '730',
        'norender': '1',
        'currency': '7'
    }

    try:
        response = session.get('https://steamcommunity.com/market/search/render/', params=payload, cookies=cookies, headers=headers)
        response.raise_for_status()
        time.sleep(6)
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data for {sticker_name}: {e}")
        return None

def process_data(data, sticker_name):
    filtered_data = []
    for result in data.get('results', []):
        filtered_entry = {
            'hash_name': result.get('hash_name'),
            'sell_price_text': result.get('sell_price_text'),
            'classid': result['asset_description'].get('classid'),
            'icon_url': result['asset_description'].get('icon_url')
        }
        filtered_data.append(filtered_entry)
    
    filtered_sticker_data[sticker_name] = filtered_data
    return filtered_data

def main():
    cookies = {'cookie': 'insert_the_cookies_here'}
    previous_data = load_previous_data('filtered_sticker_prices.json')  # Load previous data

    # Use persistent session
    with requests.Session() as session:
        for sticker_name in stickers:
            user_agent = user_agent_rotator.get_random_user_agent()
            headers = {'User-Agent': user_agent}

            data = fetch_sticker_data(sticker_name, session, headers, cookies)
            time.sleep(2)
            if data:
                filtered_data = process_data(data, sticker_name)

                if filtered_data:
                    encoded_sticker_name = urllib.parse.quote(sticker_name)
                    sticker_url = f"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20{encoded_sticker_name}"
                    
                    message = f"**Стікер: [{sticker_name}]({sticker_url})**:\n\n"
                    for entry in filtered_data:
                        # Check if the skin is new compared to the previous data
                        is_new = sticker_name not in previous_data or \
                                 not any(prev_entry['hash_name'] == entry['hash_name'] for prev_entry in previous_data.get(sticker_name, []))
                        new_tag = " ** #NEW# **" if is_new else ""
                        
                        message += (f"- [{entry['hash_name']}]("
                                    f"https://steamcommunity.com/market/listings/730/{urllib.parse.quote(entry['hash_name'])})"
                                    f" : {entry['sell_price_text']}{new_tag}\n")
                    
                    send_telegram_message(message)
                    time.sleep(2)
                 
         

    # Save the result to a file
    with open('filtered_sticker_prices.json', 'w') as json_file:
        json.dump(filtered_sticker_data, json_file, indent=4)

    logging.info("Data saved successfully!")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
