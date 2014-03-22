
import random

ts = 15

for t in range(ts):

    a = random.randint(0, 10)
    b = random.randint(0, 10)
    c = random.randint(0, 10)

    with open('%02d.in' % t, 'w') as f:
        f.write('%d\n%d\n%d\n' % (a, b, c))

    with open('%02d.out' % t, 'w') as f:
        f.write('%d\n' % (30 * a + 25 * b + 20 * c))

