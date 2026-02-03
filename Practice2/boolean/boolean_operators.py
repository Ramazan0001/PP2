#1
x = "Hello"
y = 15

print(bool(x))
print(bool(y))
#2
print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))
#3
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))


#4
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))


#5
x = 200
print(isinstance(x, int))

