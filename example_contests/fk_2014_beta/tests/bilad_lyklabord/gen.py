
import random
import string
import itertools

ts = [
    ('manual', 'x' * 2),
    ('manual', 'a  b'),
    ('random', 1),
    ('create', 1),
    ('random', 2),
    ('create', 2),
    ('random', 5),
    ('create', 5),
    ('random', 10),
    ('create', 10),
    ('random', 20),
    ('create', 20),
    ('random', 30),
    ('create', 30),
    ('manual', 'x' * 100),
    ('random', 100),
    ('create', 100),
    ('manual', 'x' * 100 + 'y' + 'z' * 100),
    ('manual', 'x' * 100 + 'y' * 2 + 'z' * 100),
    ('random', 1000),
    ('create', 1000),
]

for i, (t, n) in enumerate(ts):
    if t == 'random':
        res = ''
        for _ in range(n):
            res += random.choice(string.ascii_lowercase)
    elif t == 'create':
        res = ''
        for _ in range(n):
            cur = random.choice(string.ascii_lowercase)
            if random.randint(0, 99) < 80:
                res += cur
            else:
                m = random.randint(2, 10)
                res += cur * m
    elif t == 'manual':
        res = n

    with open('%02d.in' % i, 'w') as f:
        f.write(res + '\n')

    with open('%02d.out' % i, 'w') as f:
        f.write(''.join( k for k,_ in itertools.groupby(res) ) + '\n')

