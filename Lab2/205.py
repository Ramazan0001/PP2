a = int(input())
n =  False
while a > 1:
   if a % 2!=0:
       break
   a//= 2
if a == 1:
    n = True

if n:
    print('YES')
else:
    print('NO')