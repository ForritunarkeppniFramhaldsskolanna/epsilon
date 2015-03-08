
import random

start = 6
ts = [
    ('valid', 10),
    ('valid', 30),
    ('valid', 50),
    ('valid', 80),
    ('valid', 100),
    ('almost valid', 10),
    ('almost valid', 30),
    ('almost valid', 50),
    ('almost valid', 80),
    ('almost valid', 100),
    ('random', 10),
    ('random', 30),
    ('random', 50),
    ('random', 80),
    ('random', 100),
]

for no, (t, n) in enumerate(ts):

    arr = [ [ '.' for j in range(n) ] for i in range(n) ]

    if t == 'valid':

        cnt = random.randint(0, n*n//2)
        for _ in range(cnt):
            x = random.randint(1, n - 2)
            y = random.randint(1, n - 2)
            sps = [ (x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1) ]

            if all( arr[nx][ny] == '.' for nx,ny in sps ):
                for nx,ny in sps:
                    arr[nx][ny] = '#'

    elif t == 'almost valid':

        cnt = random.randint(0, n*n//2)
        for _ in range(cnt):
            x = random.randint(1, n - 2)
            y = random.randint(1, n - 2)
            sps = [ (x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1) ]

            for nx,ny in sps:
                arr[nx][ny] = '#'

    elif t == 'random':

        cnt = random.randint(0, n*n)
        for _ in range(cnt):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            arr[x][y] = '#'

    with open('%02d.in' % (start + no), 'w') as f:
        f.write('%d\n' % n)
        for row in arr:
            f.write('%s\n' % ''.join(row))

