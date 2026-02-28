#1
x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)

#2
x = abs(-7.25)

print(x)

#3
x = pow(4, 3)

print(x)

#4
import math

x = math.sqrt(64)

print(x)
#5
import math
#Round a number upward to its nearest integer
x = math.ceil(1.4)
#Round a number downward to its nearest integer
y = math.floor(1.4)
print(x)
print(y)
#6
import math

x = math.pi

print(x)


#Task1
degree = 15
radian = degree * math.pi / 180

print( round(radian, 6))

#Task2
height = 5
a = 5
b = 6

area = (a + b) / 2 * height

print( area)

#Task3
n = 4
s = 25
area = (n * s * s) / (4 * math.tan(math.pi / n))

print(round(area))

#Task4
base = 5
height = 6
area = base * height
print(float(area))