
import random

ts = [
    (5, 5, 'random'),
    (5, 5, 'random'),
    (5, 5, 'random'),
    (5, 5, 'spegilmynd'),
    (5, 5, 'spegilmynd'),
    (5, 5, 'spegilmynd'),
    (6, 5, 'random'),
    (6, 5, 'random'),
    (6, 5, 'random'),
    (6, 5, 'spegilmynd'),
    (6, 5, 'spegilmynd'),
    (6, 5, 'spegilmynd'),
    (5, 6, 'random'),
    (5, 6, 'random'),
    (5, 6, 'random'),
    (5, 6, 'spegilmynd'),
    (5, 6, 'spegilmynd'),
    (5, 6, 'spegilmynd'),
    (6, 6, 'random'),
    (6, 6, 'random'),
    (6, 6, 'random'),
    (6, 6, 'spegilmynd'),
    (6, 6, 'spegilmynd'),
    (6, 6, 'spegilmynd'),
]

for no, (n, m, tp) in enumerate(ts):

    arr = [ [ random.choice(['.', '#']) for j in range(m) ] for i in range(n) ]

    if tp == 'spegilmynd':

        for i in range(n):
            for j in range(m//2):
                arr[i][m - j - 1] = arr[i][j]

    with open('%02d.in' % no, 'w') as f:
        f.write('%d %d\n' % (n, m))
        for i in range(n):
            for j in range(m):
                f.write(arr[i][j])

            f.write('\n')

