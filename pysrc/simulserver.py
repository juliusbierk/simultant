import json
from collections import Counter
import numpy as np
import torch
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
from db import create_model, get_models_names, get_all_models, create_dataset, get_data_names
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


async def data_list(request):
    return web.json_response(get_data_names())


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

    example = None
    filenames = []
    has_header = json.loads(data['has_header'])
    commit_data = json.loads(data['commit_data'])
    multiple_x_axes = json.loads(data['multiple_x_axes'])

    for fname in data:
        if not fname.startswith('file_'):
            continue
        f = data[fname].file.read().decode('latin-1')
        fname = fname[5:]
        filenames.append(fname)

        if not commit_data and len(filenames) > 1:
            continue

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(f)
        if has_header is None:
            has_header = sniffer.has_header(f)

        rows = [r for r in csv.reader(f.split('\n'), dialect=dialect) if len(r) > 0]

        if has_header:
            header = rows[0]
            rows = rows[1:]
        else:
            header = ['x'] + [f'#{i}' for i in range(1, len(rows[0]))]

        if commit_data:
            try:
                num_rows = np.array([[np.nan if x.strip() == '' else np.double(x) for x in r] for r in rows])
            except ValueError:
                return web.json_response({'success': False, 'error': 'Data contains non-numerical entries.'})

            if multiple_x_axes:
                for i in range(0, num_rows.shape[1], 2):
                    x = num_rows[:, i]
                    y = num_rows[:, i + 1]
                    mask = np.isnan(y)
                    dataset = {'parent_name': fname, 'name': header[i], 'x': list(x[mask]), 'y': list(y[mask]),
                               'orig_x': list(x[mask]), 'orig_y': list(y[mask])}
                    create_dataset(header[i + 1], fname, dataset)
            else:
                x = num_rows[:, 0]
                for i in range(1, num_rows.shape[1]):
                    y = num_rows[:, i]
                    mask = np.isnan(y)
                    dataset = {'parent_name': fname, 'name': header[i], 'x': list(x[mask]), 'y': list(y[mask]),
                               'orig_x': list(x[mask]), 'orig_y': list(y[mask])}
                    create_dataset(header[i], fname, dataset)

        else:
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

            example = {'header': header, 'has_header': has_header, 'data': rows, 'fname': fname}

    if commit_data:
        return web.json_response({'success': True, 'error': None})
    else:
        res = {'filenames': filenames, 'example': example}
        return web.json_response(res)


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
          ('/data_list', data_list),
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
