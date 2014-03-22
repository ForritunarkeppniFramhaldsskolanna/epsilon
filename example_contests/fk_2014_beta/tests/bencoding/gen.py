
import random
import string

def random_partition(n, k, init=1):
    n -= k * init
    res = [ init for _ in range(k) ]
    for _ in range(n):
        res[random.randint(0, k - 1)] += 1

    return res

def rand_str():
    n = random.randint(0,10)
    return ''.join([ random.choice(string.ascii_letters + string.digits + ' ') for _ in range(n) ])

def gen(k):

    if k == 1:
        r = random.randint(0, 99)
        if r < 40:
            return random.randint(0,100000)
        elif r < 80:
            return rand_str()
        elif r < 90:
            return []
        else:
            return {}
    else:
        r = random.randint(0, 1)
        if r == 0 or k == 2:
            cnt = random.randint(1, k-1)
            pt = random_partition(k - 1, cnt, 1)
            return [ gen(pt[i]) for i in range(cnt) ]
        else:
            cnt = random.randint(1, (k - 1)//2)
            pt = random_partition(k - 1, cnt, 2)
            return { rand_str(): gen(pt[i] - 1) for i in range(cnt) }

def encode1(x):
    if type(x) is int:
        return 'i%de' % x
    elif type(x) is str:
        return '%d:%s' % (len(x), x)
    elif type(x) is list:
        return 'l%se' % ''.join( encode1(t) for t in x )
    elif type(x) is dict:
        res = list(x.items())
        random.shuffle(res)
        return 'd%se' % ''.join( '%s%s' % (encode1(k), encode1(v)) for k,v in res )
    else:
        assert False

def encode2(x):
    if type(x) is int:
        return '%d' % x
    elif type(x) is str:
        return '"%s"' % x
    elif type(x) is list:
        return '[%s]' % ','.join( encode2(t) for t in x )
    elif type(x) is dict:
        res = list(x.items())
        random.shuffle(res)
        return '{%s}' % ','.join( '%s:%s' % (encode2(k), encode2(v)) for k,v in res )
    else:
        assert False

ts = [
    -1,
    -1,
    -1,
    -1,
    1, 1,
    2, 2,
    3, 3,
    5, 5,
    8, 8,
    10, 10,
    20,
    40,
    80,
    100,
    100,
    100,
    100,
    100,
]

for i, k in enumerate(ts):
    if k == -1:
        continue

    x = gen(k)

    with open('%02d.in' % i, 'w') as f:
        f.write(encode1(x) + '\n')

    with open('%02d.out' % i, 'w') as f:
        f.write(encode2(x) + '\n')

