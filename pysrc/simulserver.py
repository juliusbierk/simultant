from aiohttp import web
import multiprocessing


global_pipe = None

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def shuwdown(request):
    global_pipe.send('exit')
    return web.Response(text=f'Exiting')


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/name/{name}', handle),
                web.get('/exit', shuwdown),
                ])


def main(pipe):
    global global_pipe
    global_pipe = pipe
    web.run_app(app, host='localhost', port=7555)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    pipe1, pipe2 = multiprocessing.Pipe(duplex=True)
    p = multiprocessing.Process(target=main, args=(pipe2, ))
    p.start()

    pipe1.recv()
    p.terminate()
    exit()
