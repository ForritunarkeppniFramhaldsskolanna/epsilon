
from random import randint

ts = [
    (1, (1, 1000), (1, 1000)),
    (1, (1000, 1000), (1000, 1000)),
    (2, (1, 10), (1, 10)),
    (2, (1, 10), (1, 3)),
    (3, (1, 3), (1, 3)),
    (3, (1, 100), (1, 20)),
    (3, (1, 100), (1, 100)),
    (4, (1, 100), (1, 100)),
    (5, (1, 100), (1, 100)),
    (10, (1, 100), (1, 100)),
    (40, (1, 1000), (1, 100)),
    (100, (1, 1000), (1, 100)),
    (500, (1, 1000), (1, 100)),
    (600, (1, 1000), (1, 10)),
    (700, (1, 1000), (1, 100)),
    (800, (1, 1000), (1, 1000)),
    (1000, (1, 1000), (1, 1000)),
    (5000, (1, 1000), (1, 100)),
    (6000, (1, 1000), (1, 10)),
    (7000, (1, 1000), (1, 100)),
    (8000, (1, 1000), (1, 1000)),
    (10000, (1, 1000), (1, 1000)),
]


for i, (n, (a0, a1), (b0, b1)) in enumerate(ts):

    with open('%02d.in' % i, 'w') as f:
        f.write('%d\n' % n)

        for i in range(n):
            f.write('%d %d\n' % (randint(a0, a1), randint(b0, b1)))
