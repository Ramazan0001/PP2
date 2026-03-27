names = ["Ali", "Ayan", "Dana"]
scores = [90, 85, 88]

# enumerate
print("Enumerate:")
for i, name in enumerate(names):
    print(i, name)

# zip
print("\nZip:")
for n, s in zip(names, scores):
    print(n, s)

# type conversion
x = "10"
y = int(x)
z = float(x)

print("\nType conversion:")
print(y, type(y))
print(z, type(z))