def div(N):
    i = 0
    while i <= N:
        if i % 3 == 0 and i % 4 == 0:
            yield i
        i+=1
N = int(input())
for x in div(N):
    print(x,end = " " )