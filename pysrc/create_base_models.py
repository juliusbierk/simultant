import json
import torch
import inspect
from db import create_model
import dill


def tanh(x, a=1, b=0, c=1):
    """$c * tanh(a x + b)$"""
    return c * torch.tanh(a * x + b)

def sin(x, a=1, b=0, c=1):
    """$c * sin(a x + b)$"""
    return c * torch.sin(a * x + b)


def get_default_args(func):
    signature = inspect.signature(func)

    for k, v in signature.parameters.items():
        if v.default is inspect.Parameter.empty:
            assert k == 'x'

    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

def main():
    models = [tanh, sin]
    for m in models:
        name = m.__name__
        content = json.dumps(dict(args=get_default_args(m),
                                  f=dill.dumps(m).decode('latin-1'),
                                  doc=m.__doc__))

        create_model(name, content)

if __name__ == '__main__':
    main()
