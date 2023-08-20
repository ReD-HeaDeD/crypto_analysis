from model import *


def initialize_db():
    db.connect()
    db.create_tables([Coin], safe=True)
    db.close()


def save_db(): #запись данных
    for row in open('coin_list.txt').readlines():
        f = Coin.create(name=row.strip().split(':')[0],
                        price=row.strip().split(':')[1])
        f.save()


initialize_db()
save_db()