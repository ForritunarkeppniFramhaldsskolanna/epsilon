
pat = input()
n = int(input())

for _ in range(n):
    s = input()

    if '*' in pat:
        a, b = pat.split('*')
        ok = len(a+b) <= len(s) and s.startswith(a) and s.endswith(b)
    else:
        ok = s == pat

    if ok:
        print('Passar')
    else:
        print('Passar ekki')

