# views.py
from aiohttp import web
import json
import db
import datetime

async def index(request):
    return web.Response(text='Hello Aiohttp!')


async def new_user(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: " , user)

        response_obj = { 'status' : 'success' }
        # return a success json response with status code 200 i.e. 'OK'
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = { 'status' : 'failed', 'reason': str(e) }
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)


async def req_state_of_dev(request):
    async with request.app['db'].acquire() as conn:
        address = request.query['adr']
        start = request.query['start']
        stop = request.query['stop']
        #start = 1547067600
        #stop = 1555313501
        dstart = datetime.datetime.fromtimestamp(int(start))
        dstop = datetime.datetime.fromtimestamp(int(stop))
        print("req address is:", address)
        try:
            if address == 'None':
                cursor = await conn.execute(db.state_dev.select()\
                                            .where(db.state_dev.c.pub_date > dstart)\
                                            .where(db.state_dev.c.pub_date < dstop))
            else:
                cursor = await conn.execute(db.state_dev.select()\
                                            .where(db.state_dev.c.device_id == address)\
                                            .where(db.state_dev.c.pub_date > dstart)\
                                            .where(db.state_dev.c.pub_date < dstop))

            records = await cursor.fetchall()
            for row in records:
                print(row)
            response_obj = [dict(q) for q in records]
            return web.Response(text=json.dumps(response_obj, indent=4, sort_keys=False, default=str), status=200)

        except Exception as e:
            response_obj = {'status': 'failed', 'reason': str(e)}
            # return failed with a status code of 500 i.e. 'Server Error'
            return web.Response(text=json.dumps(response_obj), status=500)




