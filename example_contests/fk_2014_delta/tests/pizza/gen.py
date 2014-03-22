import sys
import random

n = int(sys.argv[1])
a = int(sys.argv[2])
b = int(sys.argv[3])

print(n)
for _ in range(n):
    print(random.randint(a, b))

