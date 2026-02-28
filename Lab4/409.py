def pow(N):
    i = 0
    while i <= N:
        yield 2**i
        i+=1
N = int(input())
for x in pow(N):
    print(x,end = " ")