from peewee import *

db = SqliteDatabase('coin.db') #драйвер базы данных


class Coin(Model):
    name = CharField()
    price = CharField()

    class Meta:
        database = db