# db.py
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, Boolean, Float, create_engine
)
from db import perimeter, state_dev, device
import datetime

meta = MetaData()




async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_state_of_device(address, conn):
    pass


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = MetaData(bind=con, reflect=True)

    return con, meta


def st_dev_sample_push():
    con.execute(state_dev.insert(), [
        {'device_id': '11', 'states_of_rays': ('n' * 72),
         'power': 100, 'pub_date': '2000-12-15 10:46:49.112+02'},
        {'device_id': '11', 'states_of_rays': ('n' * 72),
         'power': 100, 'pub_date': '2015-12-19 15:30:51.234+02'},
        {'device_id': '12', 'states_of_rays': ('n' * 72),
         'power': 100, 'pub_date': '2019-03-19 20:00:12.629+02'},
    ])


def del_st_dev():
    con.execute(state_dev.delete())


def del_all_tabs():
    con.execute(perimeter.delete())
    con.execute(device.delete())
    con.execute(state_dev.delete())

def show_dev():
    for row in con.execute(device.select()):
        print(row)

def show_perim():
    for row in con.execute(state_dev.select()):
        print(row)

def show_states():
    for row in con.execute(perimeter.select()):
        print(row)

con, meta = connect('postgres', 'nbhyfyjun', 'aiohttpdemo_polls')
print(con)
print(meta)

print('=============ALL ROWS DEVICES===========')
show_dev()
print('=============ALL ROWS PERIMETERS===========')
show_perim()
print('=============ALL ROWS STATES===========')
show_states()

print('=============MATCH===========')
cursor = con.execute(perimeter.select().where(perimeter.c.name == 'Главный'))
records = cursor.fetchall()
if records:
    print(records)
    con.execute(
        perimeter.update().values(devices='11,12').where(
            perimeter.c.name == 'Главный'))
    cursor = con.execute(perimeter.select().where(perimeter.c.name == 'Главный'))
    records = cursor.fetchall()
    print(records)
else:
    print('Dict is empty')

d = datetime.datetime(2019,3,13,13,30,00)
d1 = datetime.datetime.now()
print('time1:', d.timestamp())
print('time2:', d1.timestamp())
print(d)
print(type(d))



print('time:',d)
print('timestamp: ', d.timestamp())
k = d.timestamp()

j = datetime.datetime.fromtimestamp(k)
print(j)


q = {'adr': 11, 'conf': 1}
print(q['adr'])

q = datetime.datetime.now()
print(q)