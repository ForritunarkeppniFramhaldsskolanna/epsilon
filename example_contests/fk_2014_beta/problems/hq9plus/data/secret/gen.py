import random

ts = [

    # example tests
    ('raw', 'H9+9'),
    ('raw', 'QQQQH'),
    ('raw', '++Q+'),

    # random edge cases
    ('random', '+', 1),
    ('random', '+', 2),
    ('random', '+', 4),
    ('random', '+', 5),
    ('random', '+', 9),
    ('random', '+', 20),
    ('random', '+', 150),
    ('random', '+', 1000),

    ('random', 'H', 1),
    ('random', 'H', 2),
    ('random', 'H', 4),
    ('random', 'H', 5),
    ('random', 'H', 9),
    ('random', 'H', 20),
    ('random', 'H', 150),
    ('random', 'H', 1000),

    ('random', 'Q', 1),
    ('random', 'Q', 2),
    ('random', 'Q', 4),
    ('random', 'Q', 5),
    ('random', 'Q', 9),
    ('random', 'Q', 20),
    ('random', 'Q', 150),
    ('random', 'Q', 1000),

    ('random', '9', 1),
    ('random', '9', 2),
    ('random', '9', 4),
    ('random', '9', 5),
    ('random', '9', 9),
    ('random', '9', 20),
    ('random', '9', 150),
    ('random', '9', 1000),

    ('random', 'HQ9', 1),
    ('random', 'HQ9', 2),
    ('random', 'HQ9', 4),
    ('random', 'HQ9', 5),
    ('random', 'HQ9', 9),
    ('random', 'HQ9', 20),
    ('random', 'HQ9', 150),
    ('random', 'HQ9', 1000),

    # random
    ('random', 'HQ9+', 1),
    ('random', 'HQ9+', 2),
    ('random', 'HQ9+', 3),
    ('random', 'HQ9+', 4),
    ('random', 'HQ9+', 5),
    ('random', 'HQ9+', 6),
    ('random', 'HQ9+', 7),
    ('random', 'HQ9+', 8),
    ('random', 'HQ9+', 9),
    ('random', 'HQ9+', 10),
    ('random', 'HQ9+', 20),
    ('random', 'HQ9+', 30),
    ('random', 'HQ9+', 40),
    ('random', 'HQ9+', 50),
    ('random', 'HQ9+', 100),
    ('random', 'HQ9+', 150),
    ('random', 'HQ9+', 200),
    ('random', 'HQ9+', 300),
    ('random', 'HQ9+', 400),
    ('random', 'HQ9+', 500),
    ('random', 'HQ9+', 600),
    ('random', 'HQ9+', 700),
    ('random', 'HQ9+', 800),
    ('random', 'HQ9+', 900),
    ('random', 'HQ9+', 1000),

]


for i, t in enumerate(ts):
    s = ''

    if t[0] == 'raw':
        s = t[1]
    elif t[0] == 'random':
        s = ''.join( random.choice(t[1]) for _ in range(t[2]) )

    with open('T%02d.in' % i, 'w') as f:
        f.write('%s\n' % s)


