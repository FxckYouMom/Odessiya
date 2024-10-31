import requests

url = "https://minfin.com.ua/api/currency/rates/banks/usd/?page=1&cpp=30&city=khmelnitskiy"
response = requests.get(url=url).json()['data']

data = []
for i in response:
    if i['card']:
        bid = float(i['card']['bid'])
        ask = float(i['card']['ask'])
        data.append((i['slug'], bid, ask))

smallest_ask = sorted(data, key=lambda x: x[2])[:3]

largest_bid = sorted(data, key=lambda x: x[1], reverse=True)[:3]

formatted_smallest_ask = [f"{bank[0]}: {bank[2]:.3f}" for bank in smallest_ask]
formatted_largest_bid = [f"{bank[0]}: {bank[1]:.3f}" for bank in largest_bid]

CFULLDATA = []
CFULLDATA.append("КУПЛЯТИ КАРТА:")
CFULLDATA.extend(formatted_smallest_ask)
CFULLDATA.append("\nПРОДАВАТИ КАРТА:")
CFULLDATA.extend(formatted_largest_bid)