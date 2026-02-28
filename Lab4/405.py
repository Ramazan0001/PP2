def r(N):
    i = N
    while i >= 0:
        yield i
        i -= 1

N = int(input())

for x in r(N):
    print(x)