n = int(input())
i = 0
maximum= -1000000
numbers = input().split()
while i < n:
    b = int(numbers[i])
    i+=1
    if b > maximum:
        maximum = b

print(maximum)