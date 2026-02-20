def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

nums = list(map(int, input().split()))
primes = list(filter(lambda x: is_prime(x), nums))

if len(primes) == 0:
    print("No primes")
else:
    print(*primes)
