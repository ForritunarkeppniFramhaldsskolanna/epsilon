
import random
import string

n = random.randint(1, 20)
m = random.randint(1, 20)

keys = []
for _ in range(m):
    keys.append(''.join( random.choice(string.ascii_uppercase) for i in range(3) ))

print(n)
for _ in range(n):
    print('%s%03d %.1lf' % (random.choice(keys), random.randint(100,999), round(random.random() * 10, 1)))

