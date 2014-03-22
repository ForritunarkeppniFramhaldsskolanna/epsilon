
s = input()

if all( a < b for a, b in zip(s, s[1:]) ):
    print('fyndið')
else:
    print('ekki fyndið')

