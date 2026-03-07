import re
s = input()
result = re.findall(r"\d{2,}",s)
print(" ".join(result))