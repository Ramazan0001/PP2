import re

S = input()
P = input()
pattern = re.escape(P)
result = re.findall(pattern, S)

print(len(result))