# init_db.py
from sqlalchemy import create_engine, MetaData

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.db import perimeter, device, state_dev


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[perimeter, device, state_dev])

def drop_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[perimeter, device, state_dev])



def sample_data(engine):
    conn = engine.connect()
    conn.execute(perimeter.insert(), [
        {'id': 1,
         'number': 1,
         'enabled': 1,
         'time_last_change_state': '2019-03-15 20:00:12.629+02'}
    ])
    conn.execute(device.insert(), [
        {'id': 11, 'address': '11', 'perimeter_id': 1, 'configuration': 72, 'enabled': 1},
        {'id': 12, 'address': '12', 'perimeter_id': 1, 'configuration': 72, 'enabled': 1},
    ])
    conn.execute(state_dev.insert(), [
        {'device_id': '11', 'states_of_rays': ('n'*72),
         'power': 100, 'pub_date': '2000-12-15 10:46:49.112+02'},
        {'device_id': '11', 'states_of_rays': ('n'*72),
         'power': 100, 'pub_date': '2015-12-15 15:30:51.234+02'},
        {'device_id': '12', 'states_of_rays': ('n'*72),
         'power': 100, 'pub_date': '2019-03-15 20:00:12.629+02'},
    ])

    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    drop_tables(engine)
    create_tables(engine)
    sample_data(engine)
