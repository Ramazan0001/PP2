n = int(input())
x = list(map(int, input().split()))
y = list(map(int, input().split()))

sum = 0
for a, b in zip(x, y):
    sum += a * b

print(sum)