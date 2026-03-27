a = int(input())
n = list(input().split())

print(max((i for i in n), key=len))