import sys

def fib(n):
    a = 0
    b = 1
    i = 0
    while i < n:
        yield a
        a, b = b, a + b
        i += 1

n = int(input())

first = True
for x in fib(n):
    if not first:
        sys.stdout.write(",")
    sys.stdout.write(str(x))
    first = False