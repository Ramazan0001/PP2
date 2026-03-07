import re
text = input()
result = re.findall(r"\d{2}/\d{2}/\d{4}", text)
print(len(result))