import typing
import inspect


class MyType:
    def __init__(self):
        pass

    def __call__(self, i):
        return typing.NewType(f'{i}', typing.Any)

    def __getitem__(self, sli):
        i = sli.start
        j = sli.stop
        t = typing.NewType(f'{i}-{j}', typing.Any)
        t.i = i
        t.j = j
        return t

U = MyType()

def a(x: U[0:]):
    return x

print([[k, v.default, v.annotation.i, v.annotation.j] for k, v in inspect.signature(a).parameters.items()])



