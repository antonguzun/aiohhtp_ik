import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from random import choice
from aiohttp import web, ClientSession, ClientError
import requests

from settings import config
from routes import setup_routes


async def post_request(url, json, proxy=None):
    async with ClientSession() as client:
        try:
            async with client.post(url, json=json, proxy=proxy, timeout=60) as response:
                html = await response.text()
                return {'html': html, 'status': response.status}
        except ClientError as err:
            return {'error': err}


def get_request(url):
    try:
        res = requests.get(url)
        return {'html': res.text, 'status': res.status_code, 'url': res.url, 'original_url': url}
    except requests.RequestException:
        return


class ScraperServer:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.loop = asyncio.get_event_loop()
        self.data_to_save = deque([])
        self.example_endpoint = 'http://127.0.0.1:8000'

    async def get_urls(self, request):
        data = await request.json()
        url = data.get('url')
        if url:
            t = self.loop.run_in_executor(self.pool, get_request, url)
            t.add_done_callback(self.scrape_callback)
        return web.json_response({'Status': 'Dispatched'})

    def scrape_callback(self, return_value):
        return_value = return_value.result()
        if return_value:
            self.data_to_save.append(return_value)

    async def process_queue(self):
        while True:
            print('ok')
            await asyncio.sleep(1)

    async def start_background_tasks(self, app):
        app['dispatch'] = app.loop.create_task(self.process_queue())

    async def cleanup_background_tasks(self, app):
        app['dispatch'].cancel()
        await app['dispatch']

    async def create_app(self):
        app = web.Application()
        setup_routes(app)
        app['config'] = config
        return app

    def run_app(self):
        loop = self.loop
        app = loop.run_until_complete(self.create_app())
        app.on_startup.append(self.start_background_tasks)
        app.on_cleanup.append(self.cleanup_background_tasks)
        web.run_app(app, host=self.host, port=self.port)


if __name__ == '__main__':
    s = ScraperServer(host='127.0.0.1', port=5002)
    s.run_app()
