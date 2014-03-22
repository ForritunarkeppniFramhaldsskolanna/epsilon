
import random

ts = [
    (1,'rand'),
    (2,'rand'),
    (3,'rand'),
    (4,'rand'),
    (5,'rand'),
    (6,'rand'),
    (7,'rand'),
    (1,'incr'),
    (2,'incr'),
    (3,'incr'),
    (4,'incr'),
    (5,'incr'),
    (6,'incr'),
    (7,'incr'),
]

for i, (n, tp) in enumerate(ts):

    if tp == 'rand':
        arr = [ random.randint(-100, 100) for _ in range(n) ]
    elif tp == 'incr':

        arr = [ random.randint(-100, 100) ]
        for _ in range(n-1):
            arr.append(random.randint(arr[-1]+1, arr[-1]+100))

    with open('%02d.in' % i, 'w') as f:
        f.write('%d\n' % n)
        f.write(' '.join(str(x) for x in arr))
        f.write('\n')

    with open('%02d.out' % i, 'w') as f:
        if all( x < y for x,y in zip(arr,arr[1:]) ):
            f.write('Haekkandi\n')
        else:
            f.write('Ekki haekkandi\n')

