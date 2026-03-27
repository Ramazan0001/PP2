def even(x):
    return x % 2 == 0

r = int(input())
n = list(map(int, input().split()))
a = list(filter(even, n))
print(len(a))