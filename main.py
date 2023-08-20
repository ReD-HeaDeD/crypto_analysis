import requests

#по этой ссылке есть тонна инфы на коины и по параметру symbols находим отрезок наименования коина
url = 'https://api.binance.com/api/v3/exchangeInfo'
call = requests.get(url)
cryptocurrency = call.json()['symbols']
symbol = []
for currency in cryptocurrency:
    symbol.append(currency.get('baseAsset'))

#циклом беру по коину из symbol дописываю валюту и происходит парсинг валюты + цены в $
index = 0
while len(symbol) > index:
    coin = symbol[index] + 'USDT'
    new_url = f'https://api.binance.com/api/v3/avgPrice?symbol={coin}'
    new_call = requests.get(new_url)
    new_cryptocurrency = new_call.json()
    price = new_cryptocurrency.get('price')

    with open("coin_list.txt", "a", encoding='utf-8') as file: #запись в файл
        file.write(f'{symbol[index]}:{price}' + '\n')
    #print(symbol[index], price)

    index += 1