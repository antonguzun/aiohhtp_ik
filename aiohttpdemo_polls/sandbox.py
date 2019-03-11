# db.py
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, Boolean, Float, create_engine,
    select, delete, insert,bindparam
)
import datetime

meta = MetaData()


perimeter = Table(
    'perimeter', meta,

    Column('id', Integer, primary_key=True),
    Column('number', Integer, nullable=False),
    Column('enabled', Boolean, nullable=False),               #1 - on, 0 - off
    Column('time_last_change_state', Date, nullable=False)
)


device = Table(
    'device', meta,

    Column('id', Integer, primary_key=True),
    Column('address', Integer, nullable=False),
    Column('perimeter_id',
           Integer,
           ForeignKey('perimeter.id', ondelete='CASCADE')),
    Column('configuration', Integer, nullable=False),
    Column('enabled', Boolean, nullable=False)
)

state_dev = Table(
    'state_of_device', meta,

    Column('id', Integer, primary_key=True),
    Column('device_id',
           Integer,
           ForeignKey('device.id', ondelete='CASCADE')),
    Column('states_of_rays', String(144), nullable=False),
    Column('power', Float, nullable=False),
    Column('pub_date', Date, nullable=False)
)


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


con, meta = connect('postgres', '1234', 'aiohttpdemo_polls')
print(con)
print(meta)

print('=============ALL COL===========')
for row in con.execute(state_dev.select()):
     print(row)

print('=============MATCH===========')
#con.execute(select().where(state_dev.c.device_id == 11))

cursor = con.execute(state_dev.select())
#cursor = con.execute(state_dev.select())
d = datetime.datetime(2019,1,10)
d1 = datetime.datetime.now()
print('time1:', d.timestamp())
print('time2:', d1.timestamp())
print(d)
print(type(d))

for row in cursor:
     print(row)
     print(row[4])
     print(type(row[4]))
     if(row[4] < d):
         print('ok')
     else:
         print('not ok')

print('time:',d)
print('timestamp: ', d.timestamp())
k = d.timestamp()

j = datetime.datetime.fromtimestamp(k)
print(j)