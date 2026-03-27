n = input()
z = list(map(int, input().split()))

if all(i >= 0 for i in z):
    print("Yes")
else:
    print("No")