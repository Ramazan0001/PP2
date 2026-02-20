n = int(input())  
numbers = [input().strip() for _ in range(n)]  
freq = {}
for number in numbers:
    if number in freq:
        freq[number] += 1
    else:
        freq[number] = 1


count = 0
for value in freq.values():
    if value == 3:
        count += 1


print(count)

