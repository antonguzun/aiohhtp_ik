# views.py
from aiohttp import web
import json
from db import perimeter, state_dev, device
import datetime


async def index(request):
    return web.Response(text='Hello Aiohttp!')


async def create_perimeter(request):
    """
    create new row in data
    :param request: json with keys: id(optional) - int, name: string, devices: string
    :return: request + 200
    """
    async with request.app['db'].acquire() as conn:
        try:
            body = await request.read()
            body.decode('utf-8')
            data = json.loads(body)
            if 'id' in data:
                await conn.execute(perimeter.insert().values(id=data['id'],
                                          name=data['name'],
                                          devices=data['devices']))
            else:
                await conn.execute(perimeter.insert().values(name=data['name'],
                                          devices=data['devices']))
            #cursor = await conn.execute(perimeter.select().where(perimeter.c.name == data['name']))
            #records = await cursor.fetchall()
            #print(records)

            return web.Response(text=json.dumps(data, indent=4, sort_keys=False, default=str), status=200)
        except Exception as e:
            response_obj = {'status': 'failed', 'reason': str(e)}
            return web.Response(text=json.dumps(response_obj), status=500)


async def delete_perimeter(request):
    try:
        print("Deleting perimeter: ")
        response_obj = {'status': 'success'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def update_perimeter(request):
    try:
        print("updating perimeter: ")
        response_obj = {'status': 'success'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def state_detail_view(request):
    """
    send those data from db that match with params
    :param request: address - int number or string 'all', 'from' and 'to'- timestamp values
    :return: json array of selected devices states in time between 'from' and 'to'.
    """
    async with request.app['db'].acquire() as conn:
        address = request.query['address']
        time_from = request.query['from']
        time_to = request.query['to']
        # example:
        # address = all
        # from = 1547067600
        # to = 1555313501
        dt_from = datetime.datetime.fromtimestamp(int(time_from))
        dt_to = datetime.datetime.fromtimestamp(int(time_to))
        try:
            if address == 'all':
                cursor = await conn.execute(state_dev.select()
                                            .where(state_dev.c.pub_date > dt_from)
                                            .where(state_dev.c.pub_date < dt_to))
            else:
                cursor = await conn.execute(state_dev.select()
                                            .where(state_dev.c.device_id == address)
                                            .where(state_dev.c.pub_date > dt_from)
                                            .where(state_dev.c.pub_date < dt_to))

            records = await cursor.fetchall()
            response_obj = [dict(q) for q in records]
            return web.Response(text=json.dumps(response_obj, indent=4, sort_keys=False, default=str), status=200)

        except Exception as e:
            response_obj = {'status': 'failed', 'reason': str(e)}
            # return failed with a status code of 500 i.e. 'Server Error'
            return web.Response(text=json.dumps(response_obj), status=500)
