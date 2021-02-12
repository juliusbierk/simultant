import asyncio
import json
import numpy as np
import torch
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import aiohttp_cors
from db import create_model, get_models_names, get_all_models, create_dataset,\
    get_data_names, get_data_content, get_models_content
import db
from torchfcts import function_from_code, get_default_args, check_code_get_args, get_f_expr_or_ode
import logging
import csv
import multiprocessing
import queue
import pickle
from torchfit import torch_fit

logging.basicConfig(level=logging.WARN)
logging.root.setLevel(logging.WARN)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HOST = '127.0.0.1'
PORT = 7555

sys_print = print

DEFAULT_PLOTLY_COLORS = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                       'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                       'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                       'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                       'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

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
    kwargs = get_default_args(f, data['expr_mode'], data.get('ode_dim'))
    data['args'] = [{'name': k, 'value': v} for k, v in kwargs.items()]
    create_model(data['name'], data)

    return web.json_response({'success': True})

async def delete_model(request):
    data = await request.json()
    db.delete_model(data['name'])
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
    content = data['content']
    f_name = content['name_underscore']

    f = function_from_code(content['code'], f_name)
    kwargs = get_default_args(f, content['expr_mode'], content.get('ode_dim'))
    f = get_f_expr_or_ode(content['code'], content['expr_mode'], f_name, content.get('ode_dim_select'))

    # if not content['expr_mode']:
    #     kwargs['y0'] = torch.tensor(kwargs['y0'], dtype=torch.double)

    for k in kwargs:
        kwargs[k] = torch.tensor(kwargs[k], dtype=torch.double)

    if 'xlim' in data:
        x = torch.linspace(data['xlim'][0], data['xlim'][1], 250, dtype=torch.double)
    else:
        x = torch.linspace(0, 10, 250, dtype=torch.double)
    with torch.no_grad():
        res = f(x, **kwargs)
    mask = torch.isfinite(res)
    return mask, res, x


async def plot_data(request):
    data = await request.json()

    plot_data = []
    max_n = data.get('max_n', 250)
    for content in data['content']:
        dataset = get_data_content(content['id'])
        if len(dataset['x']) > max_n:
            skip = 1 + int(len(dataset['x']) / max_n)
        else:
            skip = 1

        x = dataset['x'][::skip]
        y = dataset['y'][::skip]
        plot_data.append({'x': x, 'y': y, 'name': dataset['name'], 'mode': 'markers',
                          'type': 'scattergl'})

    return web.json_response(plot_data)


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
                    mask = ~np.isnan(y)
                    if any(np.isnan(x[mask])):
                        return web.json_response({'success': False, 'error': 'x-axis not defined for all y-values.'})
                    dataset = {'parent_name': fname, 'name': header[i], 'x': list(x[mask]), 'y': list(y[mask]),
                               'orig_x': list(x[mask]), 'orig_y': list(y[mask])}
                    create_dataset(header[i + 1], fname, dataset)
            else:
                x = num_rows[:, 0]
                for i in range(1, num_rows.shape[1]):
                    y = num_rows[:, i]
                    mask = ~np.isnan(y)
                    if any(np.isnan(x[mask])):
                        return web.json_response({'success': False, 'error': 'x-axis not defined for all y-values.'})
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
    fit_process.terminate()
    raise GracefulExit


async def run_fit(request):
    if request.method == 'POST':
        run_fit_queue.put(await request.json())
        return web.json_response({'status': 'started'})
    return web.json_response({'error': 'must be a POST request'})

async def fit_result(request):
    try:
        fit = result_queue.get_nowait()

        # Empty iteration queue:
        await asyncio.sleep(0.01)
        try:
            while True:
                iteration_queue.get_nowait()
        except queue.Empty:
            pass

    except queue.Empty:
        # No fit result yet, check if there is a loss update:
        d = None
        try:
            while True:
                d = iteration_queue.get_nowait()
        except queue.Empty:
            pass
        return web.json_response({'status': 'no-fit', 'info': d})

    return web.json_response({'status': 'success', 'fit': fit})


async def plot_fit(request):
    data = await request.json()

    plot_data = []
    max_n = data.get('max_n', 250)

    # Generate functions
    models = {}
    for model_id, d in data['models'].items():
        m = get_models_content(d['name'])
        models[model_id] = get_f_expr_or_ode(m['code'], m['expr_mode'], m['name_underscore'], m.get('ode_dim_select'))
        models[model_id].expr_mode = m['expr_mode']
        models[model_id].ode_dim = m.get('ode_dim')

    # Plot data
    xmin = float('infinity')
    xmax = float('-infinity')
    for d_id in data['data']:
        d = data['data'][d_id]
        if d['in_use']:
            #
            dataset = get_data_content(d['id'])
            if len(dataset['x']) > max_n:
                skip = 1 + int(len(dataset['x']) / max_n)
            else:
                skip = 1
            x = dataset['x'][::skip]
            y = dataset['y'][::skip]

            if min(x) < xmin:
                xmin = min(x)
            if max(x) > xmax:
                xmax = max(x)

            plot_data.append({'x': x, 'y': y, 'name': dataset['name'], 'mode': 'markers',
                              'type': 'scattergl', 'legendgroup': d_id})

    # Plot fits
    x = np.linspace(xmin, xmax, 250)
    x_list = list(x)
    x_torch = torch.from_numpy(x)

    for i, d_id in enumerate(data['data']):
        d = data['data'][d_id]
        if d['in_use']:
            f = models[d['model']]
            is_fitted = True
            kwargs = {}
            for p in d['parameters']:
                p_id = d['parameters'][p]

                parameter = data['parameters'][p_id]

                if parameter['const']:
                    kwargs[p] = parameter['value']
                elif parameter.get('fit') is None:
                    kwargs[p] = parameter['value']
                    is_fitted = False
                else:
                    kwargs[p] = parameter['fit']

            if not f.expr_mode:
                kwargs = transform_y0_kwargs_for_ode(kwargs, f.ode_dim)

            y = f(x_torch, **kwargs).numpy()
            c = DEFAULT_PLOTLY_COLORS[i % len(DEFAULT_PLOTLY_COLORS)]
            plot_data.append({'x': x_list, 'y': list(y), 'mode': 'lines', 'showlegend': False, 'legendgroup': d_id,
                              'line': {'color': c} if is_fitted else {'color': c, 'dash': 'dash'}})

    return web.json_response(plot_data)

def transform_y0_kwargs_for_ode(kwargs, dim):
    y0 = np.ones(dim)
    for i in range(dim):
        y0[i] = kwargs[f'y0[{i}]']
        del kwargs[f'y0[{i}]']
    kwargs['y0'] = torch.from_numpy(y0)
    return kwargs


def fitter(input_queue, output_queue, status_queue):
    print('Fitting queue running')
    while True:
        fit_info = input_queue.get(True)
        logger.debug('Got fit to be run')

        # First get all parameters
        parameter_names = []
        values = []
        const_index = 0

        for parameter_id, d in fit_info['parameters'].items():
            if not d['const']:
                parameter_names.append(parameter_id)
                values.append(d['value'])
                const_index += 1

        for parameter_id, d in fit_info['parameters'].items():
            if d['const']:
                parameter_names.append(parameter_id)
                values.append(d['value'])

        logger.debug(f'#parameters = {len(fit_info["parameters"])}')
        logger.debug(f'#fit parameters = {const_index}')

        if const_index == 0:
            logger.info('No parameters to be fitted')
            output_queue.put(None)
            continue

        # Get model code
        models = {}
        for model_id, d in fit_info['models'].items():
            m = get_models_content(d['name'])
            models[model_id] = {'code': m['code'], 'expr_mode': m['expr_mode'], 'name_underscore': m['name_underscore'],
                                'ode_dim': m.get('ode_dim'), 'ode_dim_select': m.get('ode_dim_select')}

        # Get data
        data = []
        for data_id, d in fit_info['data'].items():
            if d['in_use']:
                db_data = get_data_content(d['id'])
                data.append({'x': db_data['x'], 'y': db_data['y'], 'weight': d['weight'], 'model': d['model'],
                             'parameter_indeces': {k: parameter_names.index(v) for k, v in d['parameters'].items()}})

        with open('cache.pkl', 'wb') as f:
            pickle.dump((parameter_names, values, const_index, models, data), f)

        fit = torch_fit(parameter_names, values, const_index, models, data, status_queue)

        output_queue.put(fit)


if __name__ == '__main__':
    # with open('cache.pkl', 'rb') as f:
    #     torch_fit(*pickle.load(f))
    # exit()

    # Fitter
    multiprocessing.freeze_support()
    run_fit_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    iteration_queue = multiprocessing.Queue()
    fit_process = multiprocessing.Process(target=fitter, args=(run_fit_queue, result_queue, iteration_queue))
    fit_process.start()

    # Web Server
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
              ('/delete_model', delete_model),
              ('/model_exist_check', model_exist_check),
              ('/model_list', model_list),
              ('/upload_data', upload_data),
              ('/data_list', data_list),
              ('/plot_data', plot_data),
              ('/run_fit', run_fit),
              ('/plot_fit', plot_fit),
              ('/fit_result', fit_result),
              ('/exit', shuwdown),
              ]

    methods = ['GET', 'POST', 'DELETE']
    for uri, f in routes:
        resource = cors.add(app.router.add_resource(uri))
        for m in methods:
            cors.add(resource.add_route(m, f))

    print('Python server started')
    web.run_app(app, host=HOST, port=PORT, shutdown_timeout=0.0)
    fit_process.terminate()
