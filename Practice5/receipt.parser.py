import re

file = open("raw.txt", encoding="utf-8")
text = file.read()

prices = re.findall(r"\d+\s?\d*,\d{2}", text)

datetime = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

total = re.search(r"ИТОГО:\s*\n?([\d\s,]+)", text)

payment = re.search(r"Банковская карта|Наличные", text)

print("Prices:", prices)

if total:
    print("Total:", total.group(1))

if datetime:
    print("Date and Time:", datetime.group())

if payment:
    print("Payment:", payment.group())