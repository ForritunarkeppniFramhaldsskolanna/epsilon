
import random
import string

ts = 15

for t in range(ts):
    n = random.randint(1, 20)
    out = []
    for _ in range(n):
        m = random.randint(1, 20)
        out.append(''.join( random.choice(string.ascii_lowercase) for j in range(m) ))

    with open('%02d.in' % t, 'w') as f:
        f.write('%d\n' % n)
        for _ in range(n):
            f.write('%s\n' % out[_])

    out = sorted(out)
    with open('%02d.out' % t, 'w') as f:
        for _ in range(n):
            f.write('%s\n' % out[_])

