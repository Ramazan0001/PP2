def even(N):
    i = 0
    while i <= N:
        if i % 2 == 0:
            yield i
        i += 1

N = int(input())

result = []
for x in even(N):
    result.append(str(x))

print(",".join(result))