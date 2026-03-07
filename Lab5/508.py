import re

S = input()
D = input()

print(",".join(re.split(D, S)))