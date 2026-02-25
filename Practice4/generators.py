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
