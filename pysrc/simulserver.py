from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors

HOST = '127.0.0.1'
PORT = 7555

sys_print = print

def print(*args):
    sys_print(*args, flush=True)


async def handle(request):
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



if __name__ == '__main__':
    print('Python server started')
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)
