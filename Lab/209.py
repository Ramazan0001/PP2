n = int(input())
num=(list(map(int, input().split())))
mx = max(num)
mn = min(num) 
result = []
for x in num:
    if x == mx:
        result.append(mn)
    else:
        result.append(x)
print(*result)