# db.py
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, Boolean, Float
)


meta = MetaData()


perimeter = Table(
    'perimeter', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('devices', String(400), nullable=False)
)


device = Table(
    'device', meta,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('address', Integer, nullable=False),
    Column('configuration', Integer, nullable=False)
)

state_dev = Table(
    'state_of_device', meta,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('device_id',
           Integer,
           ForeignKey('device.id', ondelete='CASCADE'),
           nullable=False),
    Column('states_of_rays', String(72), nullable=False),
    Column('power', Float, nullable=False),
    Column('pub_date', DateTime, nullable=False)
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
    await app['db'].wait_closed()


async def insert_data(data, engine):
    async with engine.acquire() as conn:
        await conn.execute(state_dev.insert(), [
            {'device_id': data['address'], 'states_of_rays': data['rays'],
             'power': data['power'], 'pub_date': data['time']}, ])
