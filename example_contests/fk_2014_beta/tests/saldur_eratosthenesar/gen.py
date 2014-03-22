ts = [

# example tests
    14,
    16,
    23,

# small numbers
    5,
    4,
    3,
    2,
    1,

# random bit bigger numbers
    10,
    20,
    31,
    32,
    33,
    46,

# perfect squares
    25,
    36,
    49,

# random incrementally larger numbers

    73,
    89,
    106,
    132,
    182,
    258,
    299,
    324,  # perfect square
    359,  # prime
    489,
    512,
    581,
    713,
    834,
    952,
    986,
    996,
    997, # largest prime in range
    998,
    999,

]


for i, n in enumerate(ts):
    with open('T%02d.in' % i, 'w') as f:
        f.write('%d\n' % n)

