n = int(input())
count = 0
i =0 
numbers = input().split()
while i < n:
    b = int(numbers[i])
    i+=1
    if  b > 0:
        count+=1

print(count)