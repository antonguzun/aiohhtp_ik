import asyncio
from aiohttp import web
from settings import config
from routes import setup_routes


async def handler(request):
    return web.Response(text="OK")


async def foo():
    while(1):
        await asyncio.sleep(0)
        print('okokok')


async def main():
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    print("======= Serving on http://127.0.0.1:8080/ ======")

    try:
        await asyncio.wait_for(foo(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    await asyncio.sleep(100*3600)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    pass
loop.close()


