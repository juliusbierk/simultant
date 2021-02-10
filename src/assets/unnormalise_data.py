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

ms = 1e-6

kp = 5e6 * ms
kn = 5.96e9 / kp * ms**nc
k2 = 3.41e17 / kp * ms**(n2 + 1)
km = 0.0

print('kp', kp)
print('kn', kn)
print('k2', k2)
print('km', km)


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

t = np.linspace(0, 50, 2500)
for i, m0 in enumerate([5, 4, 3.5, 3, 2.5, 2.0, 1.75, 1.5, 1.35, 1.2]):
    d = data[keys[i]]
    print(m0, keys[i])

    y = solve_ivp(f, (t.min(), t.max()), [0, 0], t_eval=t, args=(m0, kn, kp, km, k2, nc, n2)).y[1, :]
    plt.plot(t, y)


    new_data.append({'name': keys[i], 'x': list(1.0 * np.array(d['x'])), 'y': list(y[-1] * np.array(d['y']))})

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

