import requests
import time

buy = 10

cumulative_buy = 0
cumulative_usdt_tokens = 0
cumulative_eth_tokens = 0
cumulative_atom_tokens = 0
cumulative_btc_tokens = 0
cumulative_xrp_tokens = 0


def send_telegram_message(text):
    bot_token = '7370193223:AAHEW-96nV5xMpaFwC4ROhCN1H9u8FYAmr4'
    chat_id = '-4278021126'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
    
    response = requests.get(url)
    data = response.json()
    print(data)


while True:
    # Fetch the latest USDT to UAH price
    usdt = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH')
    usdt = float(usdt.json()['price'])
    
    # Calculate the dollar value of the buy amount
    dollar = round(buy / usdt, 10)
    
    # Fetch the latest ETH to USDT price
    usdt_eth = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
    usdt_eth = float(usdt_eth.json()['price'])
    eth_tokens = round(dollar / usdt_eth, 10)
    
    # Fetch the latest ATOM to USDT price
    usdt_atom = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ATOMUSDT')
    usdt_atom = float(usdt_atom.json()['price'])
    atom_tokens = round(dollar / usdt_atom, 10)

    # Fetch the latest BTC to USDT price
    usdt_btc = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    usdt_btc = float(usdt_btc.json()['price'])
    btc_tokens = round(dollar / usdt_btc, 10)

    # Fetch the latest XRP to USDT price
    usdt_xrp = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT')
    usdt_xrp = float(usdt_xrp.json()['price'])
    xrp_tokens = round(dollar / usdt_xrp, 10)
    
    # Update cumulative values
    cumulative_buy += buy
    cumulative_usdt_tokens += dollar
    cumulative_eth_tokens += eth_tokens
    cumulative_atom_tokens += atom_tokens
    cumulative_btc_tokens += btc_tokens
    cumulative_xrp_tokens += xrp_tokens
    
    # Calculate total tokens if bought all at once
    total_dollar = round(cumulative_buy / usdt, 10)
    total_eth_tokens = round(total_dollar / usdt_eth, 10)
    total_atom_tokens = round(total_dollar / usdt_atom, 10)
    total_btc_tokens = round(total_dollar / usdt_btc, 10)
    total_xrp_tokens = round(total_dollar / usdt_xrp, 10)
    
    send_telegram_message(f"""
Всього {cumulative_buy}Грн - {round(cumulative_usdt_tokens, 4)}$\n
BTC::\nУ {cumulative_btc_tokens} \nП {total_btc_tokens}
ETH::\nУ {cumulative_eth_tokens} \nП {total_eth_tokens}
XRP::\nУ {cumulative_xrp_tokens} \nП {total_xrp_tokens}
ATOM::\nУ {cumulative_atom_tokens} \nП {total_atom_tokens}
USDT::\nУ {cumulative_usdt_tokens}$ \nП {total_dollar}$
""")
    time.sleep(600)
