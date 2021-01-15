import inspect

import torch
from torch import sin, cos, exp, tensor, sqrt, asin, acos, ones, zeros, linspace, logspace, arange, \
    eye, zeros_like, ones_like, heaviside, cat, hstack, vstack, gather, nonzero, reshape, squeeze, take, \
    transpose, unsqueeze, abs, cosh, sinh, tan, tanh, asinh, acosh, atanh, ceil, clamp, erf, erfc, \
    floor, log, lgamma, log10, logical_and, logical_not, logical_or, logical_xor, pow, round, sigmoid, \
    argmin, argmax, amin, amax, min, max, mean, mode, median, sum, prod, std, unique, var, isinf, isnan, \
    isfinite, fft, rfft, ifft, cross, cumsum, cumprod, diag, flatten, roll, dot, det, solve, trapz

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
             "trapz": trapz}


def check_function_run(f, expr=True, ode_dim=None, ode_dim_select=None):
    error = None
    if expr:
        try:
            r = f(x=torch.tensor([1.0]))
            if hasattr(r, '__len__') and len(r) != 1:
                error = 'Output is not one-dimensional.'
        except Exception as e:
            error = str(e).replace('<string>, ', '')

    else:
        try:
            r = f(x=torch.tensor([1.0], dtype=torch.double),
                  y=torch.ones(ode_dim, dtype=torch.double))

            if len(r) != ode_dim:
                error = f'Output of function does not have required dimension ({ode_dim})'

            if not (0 <= ode_dim_select <= len(r) - 1):
                error = 'Invalid selected output dimension'

        except Exception as e:
            error = str(e).replace('<string>, ', '')

    return error


def adapt_code_default_args(code, expr=True):
    # Very ugly code that simply add "=1" to parameters that have no default value

    lines = code.split('\n')

    spl = []
    cspl = lines[0].split(',')
    if not expr and ']' in lines[0]:
        i = lines[0].index(']')
        cspl = [lines[0][:i]] + lines[0][i:].split(',')

    for x in cspl:
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


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default if v.default is not inspect.Parameter.empty else None
        for k, v in signature.parameters.items()
    }

def function_from_code(code, f_name, expr):
    code = adapt_code_default_args(code, expr)
    d = {}
    exec(code, torchfcts, d)
    f = d[f_name]
    return f
