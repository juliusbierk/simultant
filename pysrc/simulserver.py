import asyncio
from aiohttp import web, ClientSession
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
import argparse
from sys import exit

HOST = '127.0.0.1'
PORT = 7555

parser = argparse.ArgumentParser()
parser.add_argument('--start', action='store_true')
parser.add_argument('--stop', action='store_true')
args = parser.parse_args()


sys_print = print

def print(*args):
    sys_print(*args, flush=True)

if args.stop:
    async def main():
        try:
            async with ClientSession() as session:
                async with session.get(f'http://{HOST}:{PORT}/exit') as resp:
                    print(await resp.text())
        except:
            pass

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    exit()

assert args.start


async def handle(request):
    print('Test')
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def shuwdown(request):
    print('Stopping python server')
    raise GracefulExit


app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})


app.add_routes([web.get('/', handle),
                web.get('/name/{name}', handle),
                web.get('/exit', shuwdown),
                ])


for route in list(app.router.routes()):
    cors.add(route)

def main():
    print('Python server started')
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)


if __name__ == '__main__':
    main()
