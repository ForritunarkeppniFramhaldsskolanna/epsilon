
ts = [ 1, 2, 3, 4, 5, 123, 997, 4534, 1337 ]

for i, t in enumerate(ts):
    with open('%02d.in' % i, 'w') as f:
        f.write('%d\n' % t)

    with open('%02d.out' % i, 'w') as f:
        f.write('%d\n' % (2 * t))

