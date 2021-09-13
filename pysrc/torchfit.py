import queue
import time
import numpy as np
import torch
from scipy.optimize import minimize
from torchfcts import get_f_expr_or_ode, TimeoutError
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IterationCounter:
    def __init__(self):
        self.iterations = 0
        self.best_loss = float('infinity')

    def __call__(self, loss):
        if loss < self.best_loss:
            self.best_loss = loss
        self.iterations += 1


class ParameterRange:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.torch_lower = None if lower is None else torch.tensor(lower, dtype=torch.double)
        self.torch_upper = None if upper is None else torch.tensor(upper, dtype=torch.double)

    def __repr__(self):
        return f'R<{self.lower} : {self.upper}>'

    def np_forward(self, x):
        if self.lower is None and self.upper is None:
            return x

        if self.upper is None:
            return np.log(x - self.lower)

        if self.lower is None:
            return np.log(self.upper - x)

        return np.log(x - self.lower) - np.log(self.upper - x)

    def np_backward(self, x):
        if self.lower is None and self.upper is None:
            return x

        if self.upper is None:
            return np.exp(x) + self.lower

        if self.lower is None:
            return self.upper - np.exp(x)

        exp_x = np.exp(x)
        return (self.lower + self.upper * exp_x) / (1 + exp_x)

    def torch_backward(self, x):
        if self.lower is None and self.upper is None:
            return x

        if self.upper is None:
            return np.exp(x) + self.torch_lower

        if self.lower is None:
            return self.torch_upper - np.exp(x)

        exp_x = np.exp(x)
        return (self.torch_lower + self.torch_upper * exp_x) / (1 + exp_x)


class FitInterrupt(Exception):
    pass


class Callback:
    def __init__(self, interrupt_queue):
        self.last_seen = None
        self.interrupt_queue = interrupt_queue

    def __call__(self, x):
        self.last_seen = x

        if self.interrupt_queue is not None:
            try:
                self.interrupt_queue.get_nowait()
                raise FitInterrupt
            except queue.Empty:
                pass


def torch_fit(parameter_names, values, const_index, models, data,
              status_queue=None, interrupt_queue=None, method=None):
    t1 = time.time()
    for d in data:
        d['x'] = torch.tensor(d['x'], dtype=torch.double)
        d['y'] = torch.tensor(d['y'], dtype=torch.double)
        d['weight'] = 1  # could add possibility later

    for m, d in models.items():
        d['f'] = get_f_expr_or_ode(d['code'], d['expr_mode'], d['name_underscore'], d['ode_dim_select'])
        d['f'].expr_mode = d['expr_mode']
        d['f'].ode_dim = d['ode_dim']

    if method is None:
        method = 'anagrad'

    # Bounds:
    parameter_lower_bounds = [0] * const_index
    parameter_upper_bounds = [None] * const_index
    all_positive = True
    for d in data:
        f = models[d['model']]['f']
        for parameter_name, parameter_index in d['parameter_indeces'].items():
            if 'y0[' in parameter_name:
                bound = f._bounds['y0']
            else:
                bound = f._bounds[parameter_name]

            if parameter_index < const_index:
                if not(bound[1] is None and bound[0] == 0):
                    all_positive = False
                parameter_lower_bounds[parameter_index] = bound[0]
                parameter_upper_bounds[parameter_index] = bound[1]

    # Now ensure that initial values lie within bounds:
    fix_initial_values(const_index, parameter_lower_bounds, parameter_upper_bounds, values)

    # Make ParameterRange instances:
    parameter_ranges = []
    for i in range(const_index):
        parameter_ranges.append(ParameterRange(parameter_lower_bounds[i], parameter_upper_bounds[i]))

    p_np_0 = np.array(values[:const_index], dtype=np.double)
    p_const = torch.tensor(values[const_index:], dtype=torch.double)

    def eval_f(p):
        r = torch.tensor(0.0, dtype=torch.float)
        p = torch.cat((p, p_const))
        for d in data:
            f = models[d['model']]['f']
            if f.expr_mode:
                k = {k: p[i] for k, i in d['parameter_indeces'].items()}
            else:
                k = {k: p[i] for k, i in d['parameter_indeces'].items() if '[' not in k}
                k['y0'] = torch.stack([p[d['parameter_indeces'][f'y0[{i}]']] for i in range(f.ode_dim)])

            r += d['weight'] * torch.mean((f(d['x'], **k) - d['y']) ** 2)
        logger.debug(f'Loss = {r}')

        return r

    iteration_counter = IterationCounter()
    callback = Callback(interrupt_queue)

    # Transform initial guess:
    for i, r in enumerate(parameter_ranges):
        p_np_0[i] = r.np_forward(p_np_0[i])

    try:
        if method == 'anagrad':
            def loss_grad(p_np):
                try:
                    p_in = torch.from_numpy(p_np).requires_grad_()

                    if all_positive:
                        p = torch.exp(p_in)
                    else:
                        p = torch.stack([r.torch_backward(p_in[i]) for i, r in enumerate(parameter_ranges)])

                    t1 = time.time()
                    r = eval_f(p)
                    logger.debug(f'Forwards calls took {time.time() - t1} s.')

                    t1 = time.time()
                    r.backward()
                    logger.debug(f'Backwards call took {time.time() - t1} s.')

                    loss = r.detach().numpy()

                    if status_queue is not None:
                        iteration_counter(float(loss))
                        status_queue.put({'iteration': iteration_counter.iterations, 'loss': iteration_counter.best_loss})

                    return loss, p_in.grad.numpy()
                except Exception as e:
                    logger.warning('Evaluation of function failed', exc_info=e)
                    return 1e10, 0 * p_np

            res = minimize(loss_grad, p_np_0, jac=True, method='L-BFGS-B',
                           options={'ftol': 1e-6, 'disp': False}, callback=callback)

        elif method == 'nelder-mead':
            def loss(p_np):
                try:
                    p_in = torch.from_numpy(p_np)

                    if all_positive:
                        p = torch.exp(p_in)
                    else:
                        p = torch.stack([r.torch_backward(p_in[i]) for i, r in enumerate(parameter_ranges)])

                    with torch.no_grad():
                        r = eval_f(p)
                    loss = r.numpy()

                    if status_queue is not None:
                        iteration_counter(float(loss))
                        status_queue.put({'iteration': iteration_counter.iterations, 'loss': iteration_counter.best_loss})

                    return loss
                except Exception as e:
                    logger.warning('Evaluation of function failed', exc_info=e)
                    return 1e10

            min_method = {'nelder-mead': 'Nelder-Mead'}[method]
            res = minimize(loss, p_np_0, method=min_method, callback=callback)

        else:
            raise NotImplementedError

        p_opt = res.x

    except FitInterrupt:
        logger.info(f'Fit was interrupted!')
        p_opt = callback.last_seen

    # Transform final fit:
    for i, r in enumerate(parameter_ranges):
        p_opt[i] = r.np_backward(p_opt[i])

    p_res = {parameter_names[i]: float(p_opt[i]) for i in range(len(parameter_names)) if i < const_index}
    logger.debug(f'Finished fit in {time.time() - t1} seconds')
    return p_res


def fix_initial_values(const_index, parameter_lower_bounds, parameter_upper_bounds, values):
    for i in range(const_index):
        if parameter_lower_bounds[i] is None and parameter_upper_bounds[i] is None:
            continue

        if parameter_lower_bounds[i] is not None and values[i] == parameter_lower_bounds[i]:
            values[i] += 1e-10

        if parameter_upper_bounds[i] is not None and values[i] == parameter_upper_bounds[i]:
            values[i] -= 1e-10

        if parameter_lower_bounds[i] is None and parameter_upper_bounds[i] < values[i]:
            values[i] = parameter_upper_bounds[i] - 1e-10

        if parameter_upper_bounds[i] is None and values[i] < parameter_lower_bounds[i]:
            values[i] = parameter_lower_bounds[i] + 1e-10

        if parameter_lower_bounds[i] is None or parameter_upper_bounds[i] is None:
            continue

        if not (parameter_lower_bounds[i] < values[i] < parameter_upper_bounds[i]):
            values[i] = 0.5 * (parameter_lower_bounds[i] + parameter_upper_bounds[i])