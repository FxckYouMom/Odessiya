import requests
import time

buy = 10

cumulative_buy = 0
cumulative_usdt_tokens = 0
cumulative_eth_tokens = 0
cumulative_atom_tokens = 0
cumulative_btc_tokens = 0
cumulative_xrp_tokens = 0

bot_token = '7370193223:AAHEW-96nV5xMpaFwC4ROhCN1H9u8FYAmr4'
chat_id = '-4278021126'

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
    except Exception as e:
        print(f"Failed to send message: {e}")

def fetch_price(symbol):
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}')
        response.raise_for_status()
        return float(response.json()['price'])
    except Exception as e:
        print(f"Failed to fetch price for {symbol}: {e}")
        return None

while True:
    usdt = fetch_price('USDTUAH')
    if usdt is None:
        time.sleep(600)
        continue

    dollar = round(buy / usdt, 10)

    usdt_eth = fetch_price('ETHUSDT')
    usdt_atom = fetch_price('ATOMUSDT')
    usdt_btc = fetch_price('BTCUSDT')
    usdt_xrp = fetch_price('XRPUSDT')

    if None in (usdt_eth, usdt_atom, usdt_btc, usdt_xrp):
        time.sleep(600)
        continue

    eth_tokens = dollar / usdt_eth
    atom_tokens = dollar / usdt_atom
    btc_tokens = dollar / usdt_btc
    xrp_tokens = dollar / usdt_xrp

    cumulative_buy += buy
    cumulative_usdt_tokens += dollar
    cumulative_eth_tokens += eth_tokens
    cumulative_atom_tokens += atom_tokens
    cumulative_btc_tokens += btc_tokens
    cumulative_xrp_tokens += xrp_tokens

    total_dollar = round(cumulative_buy / usdt, 10)
    total_eth_tokens = round(total_dollar / usdt_eth, 10)
    total_atom_tokens = round(total_dollar / usdt_atom, 10)
    total_btc_tokens = round(total_dollar / usdt_btc, 10)
    total_xrp_tokens = round(total_dollar / usdt_xrp, 10)

    message = (f"Всього {cumulative_buy}Грн - {round(cumulative_usdt_tokens, 4)}$\n"
               f"BTC::\nУ {cumulative_btc_tokens} \nП {total_btc_tokens}\n"
               f"ETH::\nУ {cumulative_eth_tokens} \nП {total_eth_tokens}\n"
               f"XRP::\nУ {cumulative_xrp_tokens} \nП {total_xrp_tokens}\n"
               f"ATOM::\nУ {cumulative_atom_tokens} \nП {total_atom_tokens}\n"
               f"USDT::\nУ {cumulative_usdt_tokens}$ \nП {total_dollar}$")

    send_telegram_message(message)
    time.sleep(600)
