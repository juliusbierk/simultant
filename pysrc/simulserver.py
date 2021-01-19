import torch
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
from db import create_model, get_models_names, get_all_models
from torchfcts import function_from_code, get_default_args, ode_from_code, check_code_get_args
import logging

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

HOST = '127.0.0.1'
PORT = 7555

sys_print = print


def print(*args):
    sys_print(*args, flush=True)


async def check_code(request):
    data = await request.json()
    d = check_code_get_args(data['code'], data['name_underscore'], data['expr_mode'], data['ode_dim'], data['ode_dim_select'])
    return web.json_response(d)


async def add_model(request):
    data = await request.json()
    if data['expr_mode'] and 'ode_dim' in data:
        del data['ode_dim']
        del data['ode_dim_select']

    f = function_from_code(data['code'], data['name_underscore'])
    kwargs = get_default_args(f, data['expr_mode'], data['ode_dim'] if not data['expr_mode'] else None)

    data['kwargs'] = kwargs
    data['args'] = [{'name': k, 'value': v} for k, v in kwargs.items()]
    create_model(data['name'], data)

    return web.json_response({'success': True})


async def model_exist_check(request):
    data = await request.json()
    print(data['name'], get_models_names())
    return web.json_response({'exists': data['name'] in get_models_names()})


async def model_list(request):
    return web.json_response(get_all_models())


async def plot_code(request):
    data = await request.json()
    mask, res, x = plot_code_py(data)
    return web.json_response({'x': x[mask].numpy().tolist(), 'y': res[mask].numpy().tolist()})


def plot_code_py(data):
    f_name = data['name_underscore']
    f = function_from_code(data['code'], f_name)
    kwargs = get_default_args(f, data['expr_mode'], data.get('ode_dim', None))
    if not data['expr_mode']:
        f = ode_from_code(data['code'], f_name, data['ode_dim_select'])
    if 'xlim' in data:
        x = torch.linspace(data['xlim'][0], data['xlim'][1], 250, dtype=torch.double)
    else:
        x = torch.linspace(0, 10, 250, dtype=torch.double)
    res = f(x, **kwargs)
    mask = torch.isfinite(res)
    return mask, res, x


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

routes = [('/check_code', check_code),
          ('/plot_code', plot_code),
          ('/add_model', add_model),
          ('/model_exist_check', model_exist_check),
          ('/model_list', model_list),
          ('/exit', shuwdown),
          ]

methods = ['GET', 'POST', 'DELETE']
for uri, f in routes:
    resource = cors.add(app.router.add_resource(uri))
    for m in methods:
        cors.add(resource.add_route(m, f))

if __name__ == '__main__':
    # with open('tester.pickle', 'rb') as f:
    #     data = pickle.load(f)
    # for ite in range(10):
    #     print(ite)
    #     plot_code_py(data)
    # exit()

    print('Python server started')
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)
