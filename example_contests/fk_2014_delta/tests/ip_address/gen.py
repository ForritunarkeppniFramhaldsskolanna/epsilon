
import random

ts = [
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv4', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('IPv6', None),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
        ('random', 45),
]


for i, t in enumerate(ts):

    if t[0] == 'IPv4':
        inp = '.'.join( str(random.randint(0, 255)) for _ in range(4) )
        out = 'IPv4'
    elif t[0] == 'IPv6':
        inp = ':'.join( ''.join( random.choice('0123456789abcdef') for j in range(4) ) for i in range(8) )
        out = 'IPv6'
    else:
        l = random.randint(1, t[1])
        inp = ''.join( random.choice('0123456789abcdef.:') for _ in range(l) )
        out = 'Error'

    with open('%02d.in' % i, 'w') as f:
        f.write('%s\n' % inp)

    with open('%02d.out' % i, 'w') as f:
        f.write('%s\n' % out)

