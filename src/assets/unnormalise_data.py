import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def f(t, y, m0, kn, kp, km, k2, nc, n2):
    p, m = y
    mt = m0 - m

    dp = km * (m - (2 * nc - 1) * p) \
         + k2 * mt**n2 * m + kn * m**nc
    dm = 2 * (mt * kp - km * nc * (nc - 1)/2) * p \
         + n2 * k2 * mt**n2 * m + nc * kn * mt**nc

    return dp, dm

nc = 2
n2 = 2
kp = 1.0
kn = 0.596
k2 = 341
km = 0.0


def load_data():
    fname = 'onet.tsv'
    with open(fname) as fi:
        f = fi.read()

    import csv

    data = {}


    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(f)
    has_header = sniffer.has_header(f)

    rows = [r for r in csv.reader(f.split('\n'), dialect=dialect) if len(r) > 0]

    if has_header:
        header = rows[0]
        rows = rows[1:]
    else:
        header = ['x'] + [f'#{i}' for i in range(1, len(rows[0]))]

    num_rows = np.array([[np.nan if x.strip() == '' else np.double(x) for x in r] for r in rows])

    x = num_rows[:, 0]
    for i in range(1, num_rows.shape[1]):
        y = num_rows[:, i]
        mask = ~np.isnan(y)
        dataset = {'parent_name': fname, 'name': header[i], 'x': list(x[mask]), 'y': list(y[mask]),
                   'orig_x': list(x[mask]), 'orig_y': list(y[mask])}

        data[dataset['name']] = {'x': dataset['x'], 'y': dataset['y']}

    return data

data = load_data()
keys = list(data.keys())

new_data = []

plt.subplot(1, 2, 1)
t = np.linspace(0, 5, 2500)
for i, m0 in enumerate([0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.175, 0.15, 0.135, 0.12]):
    d = data[keys[i]]
    print(m0, keys[i])

    y = solve_ivp(f, (t.min(), t.max()), [0, 0], t_eval=t, args=(m0, kn, kp, km, k2, nc, n2)).y[1, :]
    plt.plot(t, y)

    new_data.append({'name': keys[i], 'x': d['x'], 'y': list(y[-1] * np.array(d['y']))})

plt.subplot(1, 2, 2)
for d in new_data:
    plt.scatter(d['x'], d['y'], s=1.5)

columns = []
length = 0
for d in new_data:
    x = [d['name']] + d['x']
    y = [d['name']] + d['y']
    if len(x) > length:
        length = len(x)
    columns.extend([x, y])


with open('unnormalised.tsv', 'w') as f:
    for i in range(length):
        row = [str(columns[j][i]) if i < len(columns[j]) else '' for j in range(len(columns))]

        f.write("\t".join(row) + '\n')


plt.show()

