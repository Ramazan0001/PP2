def cycle_k(lst, k):
    for _ in range(k):
        for item in lst:
            yield item

lst = input().split()
k = int(input())

for x in cycle_k(lst, k):
    print(x, end=" ")