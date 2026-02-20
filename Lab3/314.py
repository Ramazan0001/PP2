n = int(input())
arr = list(map(int, input().split()))
q = int(input())

for _ in range(q):
    parts = input().split()

    if parts[0] == "add":
        x = int(parts[1])
        func = lambda a, x=x: a + x

    elif parts[0] == "multiply":
        x = int(parts[1])
        func = lambda a, x=x: a * x

    elif parts[0] == "power":
        x = int(parts[1])
        func = lambda a, x=x: a ** x

    elif parts[0] == "abs":
        func = lambda a: abs(a)

    arr = list(map(func, arr))

print(*arr)
