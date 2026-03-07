import re
s = input()
result = re.findall(r"\w+",s)
print(len(result))