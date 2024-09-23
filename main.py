import requests
import json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import time
from urllib.parse import quote

software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

id_database = []

def send_telegram_message(text):
    bot_token = '7670785514:AAEFcjugKWjzYuspIx2yJ7Ue9m1SwfOPz5o'
    chat_id = '-1002452439427'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    time.sleep(0.5)
    requests.get(url, params=payload)

# List of stickers to search for
stickers = [
    "Team Dignitas Katowice 2014",
    "compLexity Gaming Katowice 2014",
    "HellRaisers Katowice 2014",
    "Ninjas in Pyjamas Katowice 2014",
    "Fnatic Katowice 2014",

    "Cloud9 DreamHack 2014",
    "Team Dignitas DreamHack 2014",
    "Fnatic DreamHack 2014",
    "Natus Vincere DreamHack 2014",
    "Virtus.Pro DreamHack 2014",
    "Ninjas in Pyjamas DreamHack 2014"

    "Titan Katowice 2015",
    "LGB eSports Katowice 2015",
    "Flipsid3 Tactics Katowice 2015",
    "Cloud9 G2A Katowice 2015",
    "Counter Logic Gaming Katowice 2015",
    "Keyd Stars Katowice 2015",
    "3DMAX Katowice 2015",

    "Flipsid3 Tactics Katowice 2015",
    "Flipsid3 Tactics MLG Columbus 2016",
    "Flipsid3 Tactics holo Cologne 2016",
    "Flipsid3 Tactics Krakow 2017",
    "Flipsid3 Tactics Atlanta 2017",
    "Flipsid3 Tactics holo MLG Columbus 2016",
    "Luminosity Gaming Cologne 2015",
    "Luminosity Gaming holo MLG Columbus 2016",
    "Luminosity Gaming MLG Columbus 2016",
    "Team Liquid holo MLG Columbus 2016",
    "Team Liquid Atlanta 2017",
    "Team Liquid Boston 2018",

    "captainMo Boston 2018",
    "somebody Boston 2018",
    "seang@res Boston 2018",
    "Twistzz Boston 2018",
    "jks Boston 2018",
    "dimasick Boston 2018",
    "ScreaM Boston 2018",

    "NiKo Krakow 2017",
    "s1mple Krakow 2017",
    "rain Krakow 2017",
    "MSL Krakow 2017",
    "FalleN Krakow 2017",
    "pashaBiceps Krakow 2017",
    "device Krakow 2017",
    "coldzera Krakow 2017",
    "karrigan Krakow 2017",
    "aizy Krakow 2017",
    "cajunb Krakow 2017",
    "k0nfig Krakow 2017",
    "JW Krakow 2017",
    "Snax Krakow 2017",
    "Zeus Krakow 2017",
    "olofmeister Krakow 2017",
    "gla1ve Krakow 2017",
    "Magisk Krakow 20170",
    "TaZ Krakow 2017"

    "electronic Atlanta 2017",
    "olofmeister Atlanta 2017",
    "s1mple Atlanta 2017",
    "nitr0 Atlanta 2017",
    "Pimp Atlanta 2017",
    "B1ad3 Atlanta 2017",
    "EliGE Atlanta 2017",
    "jdm64 Atlanta 2017",
    "device Atlanta 2017",
    "Hiko Atlanta 2017",
    "markeloff Atlanta 2017",
    "wayLander Atlanta 2017",
    "WorldEdit Atlanta 2017"

    "Group C (Foil) Cologne 2015",
    "Group B (Foil) Cologne 2015",

]
def fetch_sticker_data():
    global id_database

    # List of allowed types and weapon names
    allowed_types = ["Mil-Spec", "Restricted", "Classified", "Covert"]
    allowed_weapons = ["Ak-47", "P250", "Galil", "M4A4", "M4A1-S", "USP", "Glock", "Deagle", "Tec-9", "SSG08", "AWP", "MAC-10", "MP9"]

    for sticker_name in stickers:
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {'User-Agent': user_agent}

        payload = {
            'query': f'"{sticker_name}"',
            'start': '0',
            'count': '15',
            'search_descriptions': '1',
            'sort_column': 'price',
            'sort_dir': 'asc',
            'appid': '730',
            'norender': '1',
            'currency': '7'
        }

        cookies = {'cookie': 'insert_the_cookies_here'}

        with requests.Session() as session:
            response = session.get('https://steamcommunity.com/market/search/render/', params=payload, cookies=cookies, headers=headers)
            time.sleep(10)

            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', []):
                    item_id = result['asset_description'].get('classid')

                    # Check if the item is already in the database
                    if item_id not in id_database:
                        id_database.append(item_id)
                        if len(id_database) > 10000:
                            id_database.clear()

                        hash_name = result.get('hash_name', '').lower()
                        sell_price_text = result.get('sell_price_text', 'N/A')
                        icon_url = result['asset_description'].get('icon_url', '')
                        item_type = result['asset_description'].get('type', 'Unknown Type').lower()
                        hashname = quote(result.get('hash_name', ''))
                        fast_buy = f"https://steamcommunity.com/market/listings/730/{hashname}"

                        # Extract the price from the sell_price_text
                        price = float(result.get('sell_price', 0)) / 100  # Assuming price is in cents

                        # Determine class based on price
                        if 0 <= price < 1:
                            item_class = "A"
                        elif 1 <= price < 2:
                            item_class = "B"
                        elif 2 <= price < 5:
                            item_class = "C"
                        elif 5 <= price < 10:
                            item_class = "D"
                        elif 10 <= price < 20:
                            item_class = "E"
                        elif 20 <= price < 50:
                            item_class = "F"
                        else:
                            item_class = "X"  # For prices above 50

                        # Filter based on allowed types and weapons
                        if any(allowed_type.lower() in item_type for allowed_type in allowed_types) and \
                           any(weapon.lower() in hash_name for weapon in allowed_weapons):
                            
                            # Build message and send to Telegram
                            message = (
                                f"Скін: [{result.get('hash_name')}](https://community.akamai.steamstatic.com//economy//image//{icon_url})\n\n"
                                f"Ціна з стікером: {sell_price_text}\n"
                                f"ID: {item_id}\n"
                                f"Тип: {item_type}\n"
                                f"Клас: {item_class}\n\n"
                                f"Стікер: [{sticker_name}]\n\n"
                                f"[Fast Buy]({fast_buy})"
                            )

                            send_telegram_message(message)
                            time.sleep(0.5)
                        else:
                            # Debugging logs for items filtered out
                            #print(f"Filtered out: {hash_name}, type: {item_type}, price: {price}")
                            pass
            else:           
                #print(f"! {sticker_name}: {response.status_code}")
                pass


        
send_telegram_message("bot start work")
if __name__ == "__main__":
    while True:
        fetch_sticker_data()
        time.sleep(3)

