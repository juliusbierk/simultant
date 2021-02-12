# https://github.com/juliusbierk/torchsillyode
import torch
import numpy as np
from scipy.integrate import solve_ivp

def rk4(func, y0, t, tt):
    sol = [y0]
    i = 1
    j = 1
    T = 1.0 * tt[0]
    y = y0
    b = torch.tensor([1/6, 2/6, 2/6, 1/6], dtype=t.dtype)

    while True:
        # Choose step size
        h = tt[j] - T
        save = False
        if h + T >= t[i]:
            h = t[i] - T
            save = True
            i += 1
        else:
            j += 1

        y = _take_step(T, b, func, h, y)
        T += h

        if save:
            sol.append(y)
            if i == len(t):
                break
    y = torch.stack(sol)
    return y


def _take_step(T, b, func, h, y):
    h2 = 0.5 * h
    k0 = func(T, y)
    k1 = func(T + h2, y + h2 * k0)
    k2 = func(T + h2, y + h2 * k1)
    k3 = func(T + h, y + k2 * h)
    return y + h * (b[0] * k0 + b[1] * k1 + b[2] * k2 + b[3] * k3)


def sillyode(func, y0, t, atol=1e-9, rtol=1e-7, event=None):
    assert not t.is_cuda, 'Only works on CPU for now.'
    t = t + torch.linspace(t.min(), t.max(), len(t)) * (t[-1] - t[0]) * 1e-8  # to ensure different ts

    requires_grad = func(t[0], y0).requires_grad

    with torch.no_grad():
        def np_f(t, y):
            return func(torch.from_numpy(np.asarray(t)), torch.from_numpy(y)).numpy()

        if event is None:
            res = solve_ivp(np_f, (t.min(), t.max()), y0, t_eval=None, dense_output=not requires_grad,
                            rtol=rtol, atol=atol, events=event)
        else:
            event.terminal = True
            res = solve_ivp(np_f, (t.min(), event.X_factor * t.max()), y0, t_eval=None, dense_output=not requires_grad,
                            rtol=rtol, atol=atol, events=event)

            if len(res.t_events):
                t_event = res.t_events[0][0]

                if t_event < t.max():
                    # Silly to solve for parts of the ODE twice, but this is just too easy to not do:
                    res = solve_ivp(np_f, (t.min(), t.max()), y0, t_eval=None,
                                    dense_output=not requires_grad,
                                    rtol=rtol, atol=atol)
            else:
                t_event = t.max() + atol

        if not res.success:
            raise ArithmeticError("Could not solve ODE")

        if not requires_grad:
            y = res.sol(t.numpy())
            y = torch.from_numpy(y).t()
            assert len(y) == len(t), f'Something went wrong, needed {len(t)} evaluation points but got {len(y)}'

            if event is None:
                return y
            else:
                return y, t_event, res.sol(t_event)

    tt = torch.from_numpy(res.t)
    y = rk4(func, y0, t, tt)
    assert len(y) == len(t), f'Something went wrong, needed {len(t)} evaluation points but got {len(y)}'
    return y


if __name__ == '__main__':
    import time

    a = torch.tensor([1.0], requires_grad=True)
    b = torch.tensor([1.0], requires_grad=True)

    def f(t, y):
        r = torch.empty_like(y)
        r[0] = a * y[1]
        r[1] = -b * y[0]
        return r

    t = torch.linspace(0, 12, 300)
    y0 = torch.tensor([1.0, 0.2], requires_grad=True)

    t1 = time.time()
    y = sillyode(f, y0, t, atol=5e-7, rtol=1e-5)[:, 0]
    r = torch.sum(y**2)
    print(f'Forward time = {time.time() - t1}')
    t1 = time.time()
    r.backward()
    print(f'Backward time = {time.time() - t1}')

    print()
    print(r)
    print(a.grad, b.grad, y0.grad)

    print()
    t = t.numpy()
    y0 = y0.detach().numpy()
    def np_f(t, y):
        r = np.empty_like(y)
        r[0] = a * y[1]
        r[1] = -b * y[0]
        return r

    t1 = time.time()
    res = solve_ivp(np_f, (t.min(), t.max()), y0, t_eval=t, atol=5e-7, rtol=1e-5)
    print(f'solve_ivp time = {time.time() - t1}')
