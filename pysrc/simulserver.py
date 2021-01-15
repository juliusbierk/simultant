import json
import torch
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
from db import create_model, get_models_names, get_all_models
from torchfcts import function_from_code, check_function_run, get_default_args
import logging

HOST = '127.0.0.1'
PORT = 7555

sys_print = print


def print(*args):
    sys_print(*args, flush=True)


async def check_code(request):
    data = await request.json()
    f_name = data['name_underscore']

    try:
        f = function_from_code(data['code'], f_name, data['expr_mode'])
    except Exception as e:
        error = str(e).replace('<string>, ', '')
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

    error_on_run = check_function_run(f, expr=data['expr_mode'], ode_dim=data['ode_dim'],
                                      ode_dim_select=data['ode_dim_select'])

    return web.json_response({'error': error_on_run, 'args': [{'name': k, 'value': v} for k, v in args.items()]})


async def add_model(request):
    data = await request.json()
    if data['expr_mode'] and 'ode_dim' in data:
        del data['ode_dim']
        del data['ode_dim_select']

    f = function_from_code(data['code'], data['name_underscore'], data['expr_mode'])
    args = get_default_args(f)
    del args['x']
    if not data['expr_mode']:
        del args['y']
    data['args'] = [{'name': k, 'value': v} for k, v in args.items()]

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
    f_name = data['name_underscore']

    f = function_from_code(data['code'], f_name, data['expr_mode'])
    if 'xlim' in data:
        x = torch.linspace(data['xlim'][0], data['xlim'][1], 250)
    else:
        x = torch.linspace(0, 10, 250)
    if data['expr_mode']:
        res = f(x)
    else:
        raise NotImplementedError

    mask = torch.isfinite(res)
    return web.json_response({'x': x[mask].numpy().tolist(), 'y': res[mask].numpy().tolist()})


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
    print('Python server started')
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)
