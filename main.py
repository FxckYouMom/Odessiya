import requests
import time

def send_telegram_message(text):
    bot_token = '6346370947:AAFpePtGV60tX2PEv0rV0RK45h_VZcybx94'
    chat_id = '-1001795323643'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
    
    response = requests.get(url)
    data = response.json()
    print(data)




symbols = ['bitcoin', 'ethereum','bnb', 'solana', 'xrp', 'dogecoin',
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
        'polymesh', 'casper', 'basic-attention-token', 'jito', 'binaryx-new']

while True:
    time.sleep(600)
    for symbol in symbols:
        time.sleep(0.5)
        url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={symbol}&start=1&quoteCurrencyId=825&limit=100&category=perpetual&centerType=all&sort=cmc_rank_advanced&direction=desc&spotUntracked=true'

        print(symbol)
        response = requests.get(url).json()

        comission_dict = {'Binance': 0.07, 'Bybit': 0.05, 'MEXC': 0.05, 'KuCoin': 0.07}

        try:
            market_pairs = response["data"]["marketPairs"]
            filtered_pairs = [pair for pair in market_pairs if pair["exchangeName"] in ["Binance", "Bybit", "MEXC", "KuCoin"]]

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
                        if diff < -0.1 or diff > 0.1:
                            curse_spread = ((futures1 - futures2) / futures2) * 100
                            send_telegram_message(f"{symbol} \n\n\
{url1} \n\
{exchange1} : {rate1} \n\
Spot : {spot1} \n\
Fut : {futures1}\n\
Commission : {comission_dict[exchange1]}\n\
\n\
{url2} \n\
{exchange2} : {rate2} \n\
Spot : {spot2} \n\
Fut : {futures2}\n\
Commission : {comission_dict[exchange2]}\n\
\n\
Difference : {diff:.4f}%\n\
Time : 8H \n\
Curse spread : {curse_spread}%")    

        except KeyError:
            send_telegram_message(f"{symbol}")
