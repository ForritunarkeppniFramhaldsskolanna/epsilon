
import random

ts = [
    (-1,-1),
    (-1,-1),
    (-1,-1),
    (3,3),
    (3,3),
    (3,3),
    (4,1),
    (4,5),
    (4,20),
    (10,100),
    (10,100),
    (10,100),
    (20,100),
    (26,100),
    (26,100),
    (26,100),
    (10, 'rev'),
    (26, 'rev'),
]

for i, (n,k) in enumerate(ts):
    if n == -1:
        continue

    rev = k == 'rev'
    if rev:
        k = 2 * n - 1 - 2

    arr = [ [ '|' if col % 2 == 0 else ' ' for col in range(2*n-1) ] for row in range(k) ]

    if rev:

        for a in range(k):
            for b in range(0, min(a+1, k + 2 - a - 1)):
                if (a + b) % 2 == 0:
                    arr[a][2*b+1] = '-'

    else:
        cnt = random.randint(0, k * (n - 1))

        for _ in range(cnt):
            x, y = random.randint(0, k - 1), random.randint(0, n - 2)
            if (y == 0 or arr[x][2*(y-1)+1] == ' ') and (y == n - 2 or arr[x][2*(y+1)+1] == ' '):
                arr[x][2*y + 1] = '-'


    with open('%02d.in' % i, 'w') as f:
        f.write('%d %d\n' % (n, k))
        for row in range(k):
            f.write('%s\n' % ''.join(arr[row]))

