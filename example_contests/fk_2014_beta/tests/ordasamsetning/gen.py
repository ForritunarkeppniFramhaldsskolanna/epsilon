
import random
import string

ts = [
    ('manual', 'frum', 'umrodun'),
    ('manual', 'test', 'test'),
    ('manual', 'prufa', 'prufa'),
    ('manual', 'aaaaaaa', 'aaa'),
    ('manual', 'ab', 'ba'),
    ('manual', 'a', 'a'),
    ('manual', 'eld', 'hus'),
    ('manual', 'meow', 'moo'),
    ('random', 100, 50, 100),
    ('random', 100, 50, 100),
    ('random', 100, 50, 100),
    ('random', 100, 0, 100),
    ('random', 100, 0, 100),
    ('random', 100, 0, 100),
    ('random', 100, 50, 0),
    ('random', 100, 50, 0),
    ('random', 100, 50, 0),
    ('random', 0, 50, 100),
    ('random', 0, 50, 100),
    ('random', 0, 50, 100),
]

for i, t in enumerate(ts):

    if t[0] == 'manual':
        a = t[1]
        b = t[2]
    elif t[0] == 'random':
        a = ''.join( random.choice(string.ascii_letters) for _ in range(random.randint(0, t[1])) )
        b = ''.join( random.choice(string.ascii_letters) for _ in range(random.randint(0, t[3])) )
        c = ''.join( random.choice(string.ascii_letters) for _ in range(random.randint(0, t[2])) )

        a = a + c
        b = c + b

    assert len(a) > 0
    assert len(b) > 0

    with open('%02d.in' % i, 'w') as f:
        f.write('%s\n%s\n' % (a, b))

