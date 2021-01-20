from collections import Counter
import numpy as np
import torch
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
from db import create_model, get_models_names, get_all_models
from torchfcts import function_from_code, get_default_args, ode_from_code, check_code_get_args
import logging
import csv


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


async def upload_data(request):
    data = await request.post()
    final_upload = False

    example = None
    filenames = []

    for fname in data:
        if not fname.startswith('file_'):
            continue
        f = data[fname].file.read().decode('latin-1')
        fname = fname[5:]
        filenames.append(fname)

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(f)
        has_header = sniffer.has_header(f)

        rows = [r for r in csv.reader(f.split('\n'), dialect=dialect) if len(r) > 0]

        if has_header:
            header = rows[0]
            rows = rows[1:]
        else:
            header = None

        first_column = [x[0] for x in rows]
        if '' in first_column:
            first_column_is_time = False
        else:
            dt = np.diff([float(x) for x in first_column])
            if np.all(dt > 0):
                first_column_is_time = (np.std(dt) / np.mean(dt)) < 2.0
            else:
                first_column_is_time = False

        if not final_upload:
            cut_horizontal = False
            cut_vertical = False

            if len(rows[0]) > 7:
                rows = [r[:7] + ['&#8943;'] for r in rows]
                header = header[:7] + ['&#8943;']
                cut_horizontal = True

            if len(rows) > 7:
                rows = rows[:7] + [['<center>&#8942;</center>'] * len(rows[0])]
                cut_vertical = True

            if cut_horizontal and cut_vertical:
                rows[-1][-1] = '&#8945;'


        example = {'header': header, 'has_header': has_header,
                      'first_column_is_time': first_column_is_time, 'data': rows, 'fname': fname}

    res = {'filenames': filenames, 'example': example}

    return web.json_response(res)


def guess_seperator(s):
    options = ['\t', ';', ',']
    c = Counter(s)
    c = [c[x] for x in options]
    return options[np.argmax(c)]


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
          ('/upload_data', upload_data),
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
