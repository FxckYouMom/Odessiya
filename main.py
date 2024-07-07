import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests

API_KEY = '7029661004:AAGflxf7iCWNTWmvwjbSDKfPl4JVrC3BFwk'
bot = telebot.TeleBot(API_KEY)

ITEMS_PER_PAGE = 4
chat_id_message_map = {}
data = ["Test"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create the custom keyboard
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = KeyboardButton('/menu')
    markup.add(menu_button)
    
    bot.send_message(message.chat.id, "Бот готовий для роботи:", reply_markup=markup)

@bot.message_handler(commands=['menu'])
def send_menu(message):
    send_page(message.chat.id, 0)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error deleting menu command message: {e}")

def send_page(chat_id, page):
    global data

    if page < 0:
        page = 0
    total_pages = (len(data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if page >= total_pages:
        page = total_pages - 1
    
    markup = InlineKeyboardMarkup()
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    for i in range(start_index, min(end_index, len(data))):
        entry = data[i]
        lines = entry.split('\n')
        symbol = lines[0].strip()
        
        # Check if the spread line exists
        spread_lines = [line for line in lines if line.startswith('        Spread :')]
        if spread_lines:
            spread_line = spread_lines[0]
            spread = spread_line.split(':')[1].strip()
            button = InlineKeyboardButton(f"{symbol} | {spread}", callback_data=f"item_{i}")
        else:
            button = InlineKeyboardButton(f"{symbol} | N/A", callback_data=f"item_{i}")

        markup.row(button)

    nav_buttons = [
        InlineKeyboardButton("<", callback_data=f"page_{page - 1}" if page > 0 else "noop"),
        InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"),
        InlineKeyboardButton(">", callback_data=f"page_{page + 1}" if page < total_pages - 1 else "noop")
    ]

    markup.row(*nav_buttons)
    update_button = InlineKeyboardButton("Обновить", callback_data="option_update")
    hide_button = InlineKeyboardButton("Спрятать", callback_data="option_hide")
    markup.row(update_button, hide_button)

    if chat_id in chat_id_message_map:
        message_id = chat_id_message_map[chat_id]
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Списки обновлены:", reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error editing message: {e}")
    else:
        try:
            message = bot.send_message(chat_id, "Списки обновлены:", reply_markup=markup)
            chat_id_message_map[chat_id] = message.message_id
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error sending message: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global data

    if call.data.startswith("item_"):
        index = int(call.data.split("_")[1])
        item = data[index]
        response = f"Список элементов для Item {index + 1}:\n" + "\n".join(str(line) for line in item.split('\n'))

        markup = InlineKeyboardMarkup()
        update_button = InlineKeyboardButton("Обновить", callback_data="option_update")
        hide_button = InlineKeyboardButton("Спрятать", callback_data="option_hide")
        markup.row(update_button, hide_button)

        try:
            bot.send_message(call.message.chat.id, response, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error sending message: {e}")
    
    elif call.data.startswith("page_"):
        page = int(call.data.split("_")[1])
        send_page(call.message.chat.id, page)
    
    elif call.data == "option_update":
        symbols = [
            'bitcoin', 'ethereum','bnb', 'solana', 'xrp', 'dogecoin',
        'toncoin', 'cardano', 'shiba-inu', 'avalanche', 'tron', 'polkadot-new', 'bitcoin-cash', 'chainlink', 'near-protocol',
        'internet-computer', 'litecoin', 'uniswap', 'aptos', 'hedera', 'ethereum-classic', 'cronos', 'cosmos', 'stellar',
        'filecoin','mantle', 'okb', 'immutable-x', 'pepe', 'arbitrum', 'optimism-ethereum', 'sui', 'dogwifhat', 'kaspa', 
        'vethor-token', 'bittensor','maker', 'the-graph', 'monero', 'fetch', 'arweave', 'fantom', 'celestia', 'lido-dao',
        'core-dao', 'thorchain', 'bonk1', 'floki-inu', 'algorand', 'quant', 'sei', 'gala', 'jupiter-ag', 'flow', 'onbeam', 
        'wormhole', 'vgx-token','aave', 'bitcoin-sv', 'neo', 'ethena', 'flare', 'bittorrent-new', 'ondo-finance', 
        'singularitynet', 'chiliz', 'axie-infinity', 'gatetoken', 'the-sandbox', 'starknet-token', 'akash-network', 
        'tezos', 'ecash', 'eos', 'mina', 'worldcoin-org', 'synthetix', 'conflux-network', 'ronin', 'helium', 'safe1',
        'decentraland', 'jasmy', 'pyth-network', 'apecoin-ape','axelar', 'sats-ordinals', 'nervos-network', 'iota', 
        'kava', 'dexe', 'pancakeswap', 'tether-gold', 'osmosis', 'wemix', 'venom', 'dymension', 'astar', 'wootrade',
        'ocean-protocol', 'curve-dao-token', 'iotex', 'radix-protocol', 'altlayer', 'ethereum-name-service', 'ankr', 
        'popcat-sol', '1inch', 'aerodrome-finance', 'amp', 'pax-gold', 'trust-wallet-token', 'zilliqa', 'enjin-coin',
        'manta-network', 'pendle', 'holo', 'arkham', 'livepeer', 'siacoin', 'celo', 'ravencoin', 
        'ethereum-pow', 'rocket-pool', 'terra-luna-v2', 'galxe', 'safepal', 'qtum', 'raydium', 'compound', 'zetachain',
        'polymesh', 'casper', 'basic-attention-token', 'jito', 'binaryx-new'
        ]

        new_data = []

        for symbol in symbols:
            url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={symbol}&start=1&quoteCurrencyId=825&limit=100&category=perpetual&centerType=all&sort=cmc_rank_advanced&direction=desc&spotUntracked=true'

            try:
                response = requests.get(url).json()
                commission_dict = {'Binance': 0.07, 'Bybit': 0.05, 'MEXC': 0.05, 'KuCoin': 0.07}

                if 'data' in response and 'marketPairs' in response['data']:
                    market_pairs = response['data']['marketPairs']
                    filtered_pairs = [pair for pair in market_pairs if pair['exchangeName'] in ["Binance", "Bybit", "MEXC", "KuCoin"]]

                    funding_rates = {}

                    for pair in filtered_pairs:
                        exchange_name = pair.get('exchangeName', 'N/A')
                        funding_rate = pair.get('fundingRate', 'N/A') * 100
                        spot_price = pair.get('indexPrice', 'N/A')
                        futures_price = pair.get('price', 'N/A')
                        futures_url = pair.get('marketUrl', 'N/A')

                        funding_rates[exchange_name] = (funding_rate, spot_price, futures_price, futures_url)

                    for exchange1, (rate1, spot1, futures1, url1) in funding_rates.items():
                        for exchange2, (rate2, spot2, futures2, url2) in funding_rates.items():
                            if exchange1 != exchange2:
                                diff = rate1 - rate2
                                if (-5 < diff < -0.1) or (0.1 < diff < 5):
                                    spread = ((futures1 - futures2) / futures2) * 100
                                    entry = f"{symbol}\n\n\
{url1}\n\
{exchange1} : {rate1}\n\
Spot : {spot1}\n\
Fut : {futures1}\n\
Commission : {commission_dict[exchange1]}\n\
\n\
{url2}\n\
{exchange2} : {rate2}\n\
Spot : {spot2}\n\
Fut : {futures2}\n\
Commission : {commission_dict[exchange2]}\n\
\n\
Difference : {diff:.4f}%\n\
Time : 8H\n\
Spread : {spread:.2f}%"

                                    new_data.append(entry)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
        
        data.extend(new_data)  # Add the new data entries

        # Delete the old message first
        if call.message.chat.id in chat_id_message_map:
            old_message_id = chat_id_message_map[call.message.chat.id]
            try:
                bot.delete_message(call.message.chat.id, old_message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Error deleting old message: {e}")

        # Send a confirmation message with "Hide" button
        markup = InlineKeyboardMarkup()
        hide_button = InlineKeyboardButton("Спрятать", callback_data="option_hide")
        markup.row(hide_button)

        try:
            msg = bot.send_message(call.message.chat.id, "Списки пар:", reply_markup=markup)
            chat_id_message_map[call.message.chat.id] = msg.message_id
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error sending message: {e}")
    
    elif call.data == "option_hide":
        message_id = call.message.message_id
        try:
            bot.delete_message(call.message.chat.id, message_id)
            chat_id_message_map.pop(call.message.chat.id, None)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
    
    elif call.data == "noop":
        bot.answer_callback_query(call.id, "Текущая страница")

if __name__ == '__main__':
    try:
        print("Bot is polling...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
