def sq(a,b):
    i = 0
    for i in range(a,b+1):
        yield i ** 2

a,b= list(map(int,input().split()))


for x in sq(a,b):
    print(x)