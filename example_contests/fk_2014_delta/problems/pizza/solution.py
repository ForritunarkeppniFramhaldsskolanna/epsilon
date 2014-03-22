from math import ceil

n = int(input())
print(int(ceil(sum( int(input()) for _ in range(n)) / 8.0)))

