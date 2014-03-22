
import random
import math

start = 3

ts = [
    2,
    3,
    4,
    5,
    10,
    100,
    200,
    300,
    500,
    800,
    1000,
    1000,
    1000,
    1000,
]

def rand(a,b):
    return round(random.random() * (b - a) + a, 2)

def dist(a,b):
    return math.sqrt( pow(a[0] - b[0], 2.0) + pow(a[1] - b[1], 2.0) )

for t, cnt in enumerate(ts):

    path = [ (rand(-100, 100), rand(-100, 100)) for _ in range(cnt) ]

    with open('%02d.in' % (start + t), 'w') as f:
        f.write('%d\n' % cnt)
        for _ in range(cnt):
            f.write('%f %f\n' % path[_])

    with open('%02d.out' % (start + t), 'w') as f:
        f.write('%0.10f\n' % sum( dist(a,b) for a,b in zip(path, path[1:]) ))

