import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from multiprocessing import Pool
from datetime import datetime


def coin_listing():
    url = 'https://api.binance.com/api/v3/exchangeInfo' #по этой ссылке есть тонна инфы на коины
    call = requests.get(url, timeout=10)
    cryptocurrency = call.json()['symbols'] #и по параметру symbols находим отрезок наименования коина

    symbol = [] #циклом прошлись по всем коинам по ключу baseAsset и заносим в список symbol

    for currency in cryptocurrency:
        symbol.append(currency.get('baseAsset'))
    return symbol


x_list = coin_listing() #вызвали фукцию с соxранением в переменную


def symbol_coins(x):
    coin = x_list[x] + 'USDT' #в этой переменной save коин + его цена
    new_url = f'https://api.binance.com/api/v3/avgPrice?symbol={coin}'
    #new_call = requests.get(new_url) #устаревший формат, из за которого были проблемы ((
    session = requests.Session() #создаем запрос с сохранением параметров
    retry = Retry(connect=3, backoff_factor=0.5) #создаем объект для повторных попыток
    adapter = HTTPAdapter(max_retries=retry) #какая то крутая штука с помощью которой могу использовать повторное соед.
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    new_call = session.get(new_url)
    new_cryptocurrency = new_call.json()
    price = new_cryptocurrency.get('price') #вытянули цену коина

    with open("coin_list.txt", "a", encoding='utf-8') as file: #запись в файл
        file.write(f'{x_list[x]}:{price}' + '\n')

    return x_list[x]


if __name__ == '__main__':
    start_time = datetime.now()
    with Pool(26) as p: #multiprocessing, спасибо тебе!
        print(p.map(symbol_coins, list(range(len(x_list)))))
        print(datetime.now() - start_time)

