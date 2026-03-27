n = int(input())
x = list(map(int, input().split()))

count = sum(map(bool, x))
print(count)