def sq(N):
    i = 1 
    while i <= N: 
        yield i ** 2
        i +=1
    
N = int(input())
for x in sq(N):
    print(x)