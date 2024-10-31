import requests

url = "https://minfin.com.ua/api/currency/rates/banks/usd/?page=1&cpp=30&city=khmelnitskiy"
response = requests.get(url=url).json()['data']

data = []
for i in response:
    if i['cash']:  # Перевірка наявності інформації про картки
        bid = float(i['cash']['bid'])
        ask = float(i['cash']['ask'])
        data.append((i['slug'], bid, ask))

# Знаходимо 3 найменші ask
smallest_ask = sorted(data, key=lambda x: x[2])[:3]

# Знаходимо 3 найбільші bid
largest_bid = sorted(data, key=lambda x: x[1], reverse=True)[:3]

# Форматуємо результати
formatted_smallest_ask = [f"{bank[0]}: По {bank[2]:.3f}" for bank in smallest_ask]
formatted_largest_bid = [f"{bank[0]}: Пр {bank[1]:.3f}" for bank in largest_bid]

# Об'єднуємо результати в одне повідомлення
BFULLDATA = []
BFULLDATA.append("КУПЛЯТИ РЕАЛ:")
BFULLDATA.extend(formatted_smallest_ask)
BFULLDATA.append("\nПРОДАВАТИ РЕАЛ:")
BFULLDATA.extend(formatted_largest_bid)