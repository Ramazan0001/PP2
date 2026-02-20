n,l,r= map(int,input().split())
num = list(map(int,input().split()))
num[l-1:r] = num[l-1:r][::-1]
print(*num)


