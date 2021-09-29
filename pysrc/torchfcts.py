import inspect
import time
import traceback
import torch
from silly import sillyode
from torch import sin, cos, exp, tensor, sqrt, asin, acos, ones, zeros, linspace, logspace, arange, \
    eye, zeros_like, ones_like, heaviside, cat, hstack, vstack, gather, nonzero, reshape, squeeze, take, \
    transpose, unsqueeze, abs, cosh, sinh, tan, tanh, asinh, acosh, atanh, ceil, clamp, erf, erfc, \
    floor, log, lgamma, log10, logical_and, logical_not, logical_or, logical_xor, pow, round, sigmoid, \
    argmin, argmax, amin, amax, min, max, mean, mode, median, sum, prod, std, unique, var, isinf, isnan, \
    isfinite, fft, rfft, ifft, cross, cumsum, cumprod, diag, flatten, roll, dot, det, solve, trapz, empty, \
    empty_like
import logging
import typing
import inspect


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

torchfcts = {"sin": sin, "cos": cos, "exp": exp, "tensor": tensor, "sqrt": sqrt, "asin": asin,
             "acos": acos, "ones": ones, "zeros": zeros, "linspace": linspace, "logspace": logspace, "arange": arange,
             "eye": eye, "zeros_like": zeros_like, "ones_like": ones_like, "heaviside": heaviside,
             "cat": cat, "hstack": hstack, "vstack": vstack, "gather": gather, "nonzero": nonzero, "reshape": reshape,
             "squeeze": squeeze, "take": take,
             "transpose": transpose, "unsqueeze": unsqueeze, "abs": abs, "cosh": cosh, "sinh": sinh,
             "tan": tan, "tanh": tanh, "asinh": asinh, "acosh": acosh, "atanh": atanh, "ceil": ceil, "clamp": clamp,
             "erf": erf, "erfc": erfc,
             "floor": floor, "log": log, "lgamma": lgamma, "log10": log10, "logical_and": logical_and,
             "logical_not": logical_not, "logical_or": logical_or, "logical_xor": logical_xor, "pow": pow,
             "round": round, "sigmoid": sigmoid,
             "argmin": argmin, "argmax": argmax, "amin": amin, "amax": amax, "min": min, "max": max,
             "mean": mean, "mode": mode, "median": median, "sum": sum, "prod": prod, "std": std, "unique": unique,
             "var": var, "isinf": isinf, "isnan": isnan,
             "isfinite": isfinite, "fft": fft, "ifft": ifft, "rfft": rfft, "cross": cross, "cumsum": cumsum,
             "cumprod": cumprod, "diag": diag, "flatten": flatten, "roll": roll, "dot": dot, "det": det, "solve": solve,
             "trapz": trapz, "empty": empty, "empty_like": empty_like}


class RangeType:
    start = None
    stop = None

    def __init__(self, const=False):
        self.const = const

    def __call__(self, i):
        return typing.NewType(f'{i}', typing.Any)

    def __getitem__(self, sli):
        start = sli.start
        stop = sli.stop
        t = typing.NewType(f'{start}-{stop}', typing.Any)
        t.start = start
        t.stop = stop
        t.const = self.const
        return t


R = RangeType()
C = RangeType(const=True)


def check_function_run(f, kwargs, expr=True, ode_dim=None, ode_dim_select=None):
    tensor_kwargs = {}
    for k in kwargs:
        tensor_kwargs[k] = torch.tensor(kwargs[k], dtype=torch.double)

    error = None
    if expr:
        try:
            r = f(x=torch.tensor([1.0]), **tensor_kwargs)
            if hasattr(r, '__len__') and len(r) != 1:
                error = 'Output is not one-dimensional.'
        except Exception as e:
            logger.debug('Could not get arguments', exc_info=e)
            error = str(e).replace('<string>, ', '')

    else:
        try:
            r = f(x=torch.tensor([1.0], dtype=torch.double),
                  y=torch.tensor(kwargs['y0'], dtype=torch.double),
                               **tensor_kwargs)

            if ode_dim > 1 and len(r) != ode_dim:
                error = f'Output of function does not have required dimension ({ode_dim})'

                if not (0 <= ode_dim_select <= len(r) - 1):
                    error = 'Invalid selected output dimension'

            elif ode_dim == 1 and ode_dim_select != 0:
                error = 'Selected dimension must be zero for ODE of dimension one. '

        except Exception as e:
            logger.debug('Could not run function', exc_info=e)
            error = str(e).replace('<string>, ', '')

    return error


def check_code_get_args(code, f_name, expr_mode, ode_dim, ode_dim_select):
    try:
        f = function_from_code(code, f_name)
    except Exception as e:
        logger.debug('Could not form function', exc_info=e)
        error = str(e).replace('<string>, ', '')

        error += '\n\n' + "\n".join(traceback.format_exc(limit=0).split('\n')[1:-2])
        return {'error': error}

    try:
        kwargs = get_default_args(f, expr_mode, ode_dim)
    except Exception as e:
        logger.debug('Could not get arguments', exc_info=e)
        error = 'Could not extract arguments:\n' + str(e)
        return {'error': error}

    if not expr_mode and len(kwargs['y0']) != ode_dim:
        return {'error': 'y0 must be a list of length equal to the ODE dimension.'}

    error_on_run = check_function_run(f, kwargs, expr=expr_mode, ode_dim=ode_dim,
                                      ode_dim_select=ode_dim_select)

    bounds = get_bounds(f)
    args = [{'name': k, 'value': v, 'lower': bounds[k][0], 'upper': bounds[k][1]} for k, v in kwargs.items()]

    return {'error': error_on_run, 'args': args}


def get_default_args(func, expr, dim=1):
    signature = inspect.signature(func)

    kwargs = {
        k: v.default if v.default is not inspect.Parameter.empty else (1 if expr else (1 if k != 'y0' else [1] * dim))
        for k, v in signature.parameters.items()
    }
    del kwargs['x']
    if not expr:
        del kwargs['y']
    return kwargs


def get_bounds(func):
    signature = inspect.signature(func)
    bounds = {
        k: [0, None] if v.annotation is inspect.Parameter.empty else [v.annotation.start, v.annotation.stop]
        for k, v in signature.parameters.items()
    }
    return bounds


def get_const_bools(func):
    signature = inspect.signature(func)
    consts = {
        k: False if v.annotation is inspect.Parameter.empty else v.annotation.const
        for k, v in signature.parameters.items()
    }
    return consts


def function_from_code(code, f_name):
    d = {'R': R, 'C': C}
    exec(code, torchfcts, d)
    f: typing.Callable = d[f_name]
    f._transform = d.get('_transform')
    f._event = d.get('_event')
    f._bounds = get_bounds(f)

    return f


class TimeoutError(Exception):
    pass


def ode_from_code(code, f_name, ode_dim_select, timeout=30):
    atol = 5e-7
    rtol = 1e-5

    f = function_from_code(code, f_name)

    def ode_f(x, **kwargs):
        x_orig = x
        mask = torch.logical_and(x >= 0, torch.isfinite(x))
        x = x[mask]
        added_zero = False
        if x[0] != 0:
            added_zero = True
            x = torch.hstack((torch.tensor(0, dtype=x.dtype), x))

        start_time = time.time()

        def curied(x, y):
            if time.time() - start_time > timeout:
                logger.warning('ODE Solving timed out')
                raise TimeoutError

            r = f(x, y, **kwargs)
            if isinstance(r, torch.Tensor):
                r = (r, )
            return torch.hstack(r)

        if f._event is None:
            sol = sillyode(curied, kwargs['y0'], x, atol=atol, rtol=rtol)
            if f._transform is None:
                sol = sol[:, ode_dim_select]
            else:
                sol = f._transform(x, sol.t(), **kwargs)
        else:
            def curied_event(x, y):
                return f._event(x, y, **kwargs)
            curied_event.direction = f._event.direction if hasattr(f._event, 'direction') else 0
            curied_event.X_factor = f._event.X_factor if hasattr(f._event, 'X_factor') else 1

            sol, event_x, event_y = sillyode(curied, kwargs['y0'], x, atol=atol, rtol=rtol, event=curied_event)
            sol = f._transform(x, sol.t(), event_x, event_y, **kwargs)

        if added_zero:
            sol = sol[1:]

        res = torch.tensor(float('nan')) * torch.zeros_like(x_orig)
        res[mask] = sol

        return res

    ode_f._bounds = f._bounds

    return ode_f


def get_f_expr_or_ode(code, expr_mode, f_name, ode_dim_select):
    f = function_from_code(code, f_name)
    if not expr_mode:
        f = ode_from_code(code, f_name, ode_dim_select)
    return f