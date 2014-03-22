mem = {}
def cnt(n, e):
    if n == 0:
        return 1 if e else 0

    if (n,e) in mem:
        return mem[(n,e)]

    res = cnt(n-1, e) + cnt(n-1, not e)
    mem[(n,e)] = res
    return res

def nth(n, k, e):
    if n == 0:
        return ""

    if k < cnt(n-1, e):
        return "0" + nth(n-1, k, e)
    else:
        return "1" + nth(n-1, k-cnt(n-1, e), not e)

def parse_bin(s):
    res = 0
    for b in s:
        res *= 2
        if b == '1':
            res += 1
    return res

n = int(input())
print(parse_bin(nth(100, n-1, True)) + parse_bin(nth(100, n-1, False)))
