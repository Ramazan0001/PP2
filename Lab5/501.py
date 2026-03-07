import re

text = input()

if re.match("^Hello", text):
    print("Yes")
else:
    print("No")