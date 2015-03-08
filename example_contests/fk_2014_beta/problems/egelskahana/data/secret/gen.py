# coding: utf8
ns = range(1, 21) + [100, 101, 1337, 1338, 1339, 1340] + range(10**9, 10**9 + 10)

ans = [ 'Ég elska hana', 'Ég elska hana ekki' ]

for i, n in enumerate(ns):

    infile = open('%02d.in' % i, 'w')
    infile.write('%d\n' % n)
    infile.close()

    outfile = open('%02d.out' % i, 'w')
    outfile.write('%s\n' % ans[(n+1) % 2])
    outfile.close()
