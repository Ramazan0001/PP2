import re
s = input()
result = re.findall(r"[A-Z]",s)
print(len(result))