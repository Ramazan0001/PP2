import re
s = input()
p = input()
result = re.findall(p,s)
print(len(result))

