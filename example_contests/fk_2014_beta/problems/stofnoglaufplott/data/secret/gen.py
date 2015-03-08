import random

ts = [
    (3, 1, 40, 'gauss', 50, 50),
    (3, 1, 40, 'uniform'),
    (3, 1, 40, 'gauss', 50, 3),
    (3, 1, 40, 'gauss', 10, 5),
    (3, 1, 40, 'gauss', 80, 7),

    (3, 41, 200, 'gauss', 50, 50),
    (3, 41, 200, 'uniform'),
    (3, 41, 200, 'gauss', 50, 3),
    (3, 41, 200, 'gauss', 10, 5),
    (3, 41, 200, 'gauss', 80, 7),
]

at = 0
for t in ts:
    for _ in range(t[0]):
        n = random.randint(t[1], t[2])
        if t[3] == 'uniform': f = lambda: random.uniform(10, 99)
        elif t[3] == 'gauss': f = lambda: random.gauss(t[4], t[5])

        infile = open('%02d.in' % at, 'w')
        infile.write('%d\n' % n)
        nums = []
        while n > 0:
            cur = int(f())
            if 10 <= cur <= 99:
                nums.append(cur)
                n -= 1

        infile.write('%s\n' % ' '.join(map(str, nums)))
        infile.close()

        at += 1

