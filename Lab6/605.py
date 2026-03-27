n = input()
vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]

if any(i in vowels for i in n):
    print("Yes")
else:
    print("No")