
ts = [
    'hinstu',
    'hinsta',
    'eistu',
    'efstu',
    'feimnu',
    'abcdefghijklmnopqrstuvwxyz',
    'banani',
    'test'
]

for i, t in enumerate(ts):
    with open('%02d.in' % i, 'w') as f:
        f.write('%s\n' % t)

