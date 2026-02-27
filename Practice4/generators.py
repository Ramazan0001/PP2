#1
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)
#2
def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1

for num in count_up_to(5):
  print(num)
#3
def large_sequence(n):
  for i in range(n):
    yield i


gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))
#4

list_comp = [x * x for x in range(5)]
print(list_comp)

gen_exp = (x * x for x in range(5))
print(gen_exp)
print(list(gen_exp))

#5
def echo_generator():
  while True:
    received = yield
    print("Received:", received)

gen = echo_generator()
next(gen)  # Prime the generator
gen.send("Hello")
gen.send("World")


#Task1
def square(N):
    i = 0
    while i <= N:
        yield i * i
        i += 1

N = int(input())
for x in square_up_to(N):
    print(x)

#Task2
def evennumbers(n):
    i = 0
    while i <= n:
        if i % 2 == 0:
            yield i
        i += 1

n = int(input())
result = []

for x in evennumbers(n):
    result.append(str(x))

print(",".join(result))

#Task3
def divisible(n):
    i = 0
    while i <= n:
        if i % 3 == 0 and i % 4 == 0:
            yield i
        i += 1

n = int(input())

for x in divisible(n):
    print(x)

#Task4
def squares(a, b):
    i = a
    while i <= b:
        yield i * i
        i += 1

a,b= int(input())

for value in squares(a, b):
    print(value)
 
#Task5
def countdown(n):
    i = n
    while i >= 0:
        yield i
        i -= 1

n = int(input())

for x in countdown(n):
    print(x)