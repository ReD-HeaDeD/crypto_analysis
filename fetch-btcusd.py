#!/usr/bin/env python3

import datetime
import time
import requests
import json
import numpy as np
import pandas as pd

pair = 'BTCUSDT'
BTC = 27448.175

URI_TEMPLATE = 'https://api.binance.com/api/v1/klines?symbol=%s&interval=1d&limit=500&startTime={start}&endTime={end}' % pair
data = []

#определенная дата в переменной 2023-01-01 00:00:00
end = datetime.datetime(year=2023, month=1, day=1)
end_timestamp = int(end.timestamp() * 1000)

#текущая дата 2023-06-21 06:46:01.832017
start = datetime.datetime.utcnow()
start_timestamp = int(start.timestamp() * 1000)

#в ссылку URI_TEMPLATE подставляем временные значения
uri = URI_TEMPLATE.format(start=end_timestamp, end=start_timestamp)
print(uri)
resp = requests.get(uri).json()
print(pair, len(resp))
data += resp

list_of_coin_averages = []
index = 0
while len(data) > index:
    i = data[index]
    print(f'цена MAX: {float(i[2])}, цена MIN: {float(i[3])}')
    sq = (float(i[2]) + float(i[3])) / 2
    list_of_coin_averages.append(sq)
    print(f'среднеквадратичное: {sq}')
    index += 1
print(list_of_coin_averages)

Rf = 4.7
Rp = BTC - list_of_coin_averages[0]
print(f'доходность портфеля {Rp}')

average_value = sum(list_of_coin_averages) / len(list_of_coin_averages)
print(average_value)

value = 0
for element in list_of_coin_averages:
    value += (element - average_value) ** 2
Qr = sum((x - average_value) ** 2 for x in list_of_coin_averages) / max(1, len(list_of_coin_averages) - 1)
print(f'дисперсия: {Qr}')
S = (Rp - Rf) / Qr
print(S)
#print(average_value / Qr)
#print(BTC - list_of_coin_averages[0])