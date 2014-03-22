import random
import string

ts = 15

for t in range(ts):

    n = random.randint(5, 50)
    s = ''.join( random.choice(string.ascii_letters + string.digits + ' ')  for _ in range(n) )

    assert s[0] != ' ' and s[-1] != ' '

    with open('%02d.in' % t, 'w') as f:
        f.write('%s\n' % s)

