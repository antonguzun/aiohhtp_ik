import asyncio
from aiohttp import web
from .settings import config
from .routes import setup_routes

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def foo():
    while(1):
        await asyncio.sleep(0)
        print('okokok')

async def app_factory():
    await foo()
    app = web.Application()
    setup_routes(app)
    return app

web.run_app(app_factory())