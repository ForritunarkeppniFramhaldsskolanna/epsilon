
import random

ts = [
    (-1, -1),
    (-1, -1),
    (-1, -1),
    (3, 0.0),
    (3, 0.5),
    (3, 1.0),
    (6, 0.0),
    (6, 0.5),
    (6, 1.0),
    (10, 0.1),
    (10, 0.2),
    (10, 0.4),
    (50, 0.05),
    (50, 0.1),
    (50, 0.2),
    (100, 0.02),
    (100, 0.1),
    (100, 0.2),
]

for t, (n, mp) in enumerate(ts):

    if n == -1:
        continue

    ms = [ (i,j) for i in range(n) for j in range(i+1, n) if random.random() < mp ]

    random.shuffle(ms)

    with open('%02d.in' % t, 'w') as f:
        f.write('%d %d\n' % (n, len(ms)))

        for a, b in ms:
            if random.randint(0, 1) == 0:
                f.write('%d %d\n' % (a+1, b+1))
            else:
                f.write('%d %d\n' % (b+1, a+1))

