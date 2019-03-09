# views.py
from aiohttp import web
import json
import db


async def index(request):
    return web.Response(text='Hello Aiohttp!')


async def sand(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.state_dev.select())
        records = await cursor.fetchall()
        for row in records:
            print(row)
        response_obj = [dict(q) for q in records]
        return web.Response(text=json.dumps(response_obj, indent=4, sort_keys=True, default=str), status=200)


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


async def get_data(request):
    try:
        # happy path where name is set
        ik_adr = request.query['address']
        # Process our new user
        print("received request with address: " , ik_adr)

        response_obj = { 'status' : 'success' , 'a' : 'a'}
        # return a success json response with status code 200 i.e. 'OK'
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = { 'status' : 'failed', 'reason': str(e) }
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def result(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))
