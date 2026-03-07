import re
text = input()
match = re.search(r"Name: (.+), Age: (\d+)", text)
print(match.group(1), match.group(2))