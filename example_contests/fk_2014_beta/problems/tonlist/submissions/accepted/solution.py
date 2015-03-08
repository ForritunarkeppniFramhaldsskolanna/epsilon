
pat = raw_input()
n = int(raw_input())

for _ in range(n):
    s = raw_input()

    if '*' in pat:
        a, b = pat.split('*')
        ok = len(a+b) <= len(s) and s.startswith(a) and s.endswith(b)
    else:
        ok = s == pat

    if ok:
        print('Passar')
    else:
        print('Passar ekki')

