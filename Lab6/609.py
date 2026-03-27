n = int(input())
x = list(input().split())
y = list(input().split())

d = dict(zip(x, y))
z = input()

if z in d:
    print(d[z])
else:
    print("Not found")