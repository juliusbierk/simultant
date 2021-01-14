from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
import inspect
import torch
from torchfcts import torchfcts


HOST = '127.0.0.1'
PORT = 7555


sys_print = print

def print(*args):
    sys_print(*args, flush=True)

def adapt_code_default_args(code, expr=True):
    # Very ugly code that simply add "=1" to parameters that have no default value

    lines = code.split('\n')

    spl = []
    for x in lines[0].split(','):
        if ')' in x:
            xspl = x.split(')')
            for x2 in xspl:
                spl.append(x2)
                spl.append(')')
            del spl[-1]
        else:
            spl.append(x)
        spl.append(',')
    del spl[-1]

    i0 = 2 if expr else 3
    for i in range(i0, len(spl) - 1):
        if spl[i] == ')':
            break
        if spl[i] !=',' and '=' not in spl[i]:
            spl[i] = spl[i] + '=1'
    lines[0] = "".join(spl)

    return "\n".join(lines)


def check_function_run(f, expr=True):
    error = None
    if expr:
        try:
            f(x=torch.tensor([1.0]))
        except Exception as e:
            error = str(e)
    else:
        print('NOT IMPLEMENTED YET')

    return error

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default if v.default is not inspect.Parameter.empty else None
        for k, v in signature.parameters.items()
    }

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def check_code(request):
    data = await request.json()
    code = adapt_code_default_args(data['code'], expr=data['expr_mode'])

    try:
        d = {}
        exec(code, torchfcts, d)
        f = d[data['name_underscore']]
    except Exception as e:
        error = 'Could not parse python function:\n' + str(e)
        return web.json_response({'error': error})

    try:
        args = get_default_args(f)
    except Exception as e:
        error = 'Could not extract arguments:\n' + str(e)
        return web.json_response({'error': error})

    if 'x' not in args:
        return web.json_response({'error': "Error: `x` must be an argument."})
    del args['x']

    if not data['expr_mode']:
        if 'y' not in args:
            return web.json_response({'error': "Error: `y` must be an argument for ODEs."})
        del args['y']

    error_on_run = check_function_run(f, expr=data['expr_mode'])
    return web.json_response({'error': error_on_run, 'args': [{'name': k, 'value': v} for k, v in args.items()]})

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

routes = [('/', handle),
           ('/check_code', check_code),
           ('/exit', shuwdown),
           ]

methods = ['GET', 'POST', 'DELETE']
for uri, f in routes:
    resource = cors.add(app.router.add_resource(uri))
    for m in methods:
        cors.add(resource.add_route(m, f))


if __name__ == '__main__':
    print('Python server started')
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)
