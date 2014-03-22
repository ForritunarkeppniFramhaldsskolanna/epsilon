
import random

ts = 15

for t in range(ts):
    a = random.randint(0, 99)
    b = random.randint(0, 99)
    c = random.randint(0, 99)

    with open('%02d.in' % t, 'w') as f:
        f.write("%d %d %d\n" % (a, b, c))

    with open('%02d.out' % t, 'w') as f:
        if (a <= b <= c) or (a >= b >= c):
            f.write("Milli\n")
        else:
            f.write("Ekki Milli\n")

