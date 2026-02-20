#1
a = int(input())
i = 0
pos = 0
mx = -10**9
numbers = input().split()
while i < a:
    b = int(numbers[i])
    i+=1
    if b > mx:
        mx = b
        pos = i+1
    i+=1

print(pos)   
#2
a = int(input())
i = 0
pos = 0
mx = -10**9
numbers = input().split()

while i < a:
    b = int(numbers[i])
    if b > mx:
        mx = b
        pos = i + 1  
    i += 1

print(pos)

     