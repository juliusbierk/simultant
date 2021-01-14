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
