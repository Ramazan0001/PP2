s = input().strip()

to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}
to_word = {
    "0": "ZER", "1": "ONE", "2": "TWO", "3": "THR", "4": "FOU",
    "5": "FIV", "6": "SIX", "7": "SEV", "8": "EIG", "9": "NIN"
}
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"
left, right = s.split(op)

a = ""
for i in range(0, len(left), 3):
    a += to_digit[left[i:i+3]]
a = int(a)

b = ""
for i in range(0, len(right), 3):
    b += to_digit[right[i:i+3]]
b = int(b)

if op == "+":
    ans = a + b
elif op == "-":
    ans = a - b
else:
    ans = a * b

ans_str = str(ans)
out = ""
for ch in ans_str:
    out += to_word[ch]

print(out)
