import re
#1

text = "abbb"
if re.fullmatch("ab*", text):
    print("Match")
else:
    print("No match")

#2
text = "abb"

if re.fullmatch("ab{2,3}", text):
    print("Match")
else:
    print("No match")

#3

text = "hello_world python_regex Test"

result = re.findall("[a-z]+_[a-z]+", text)

print(result)

#4
import re

text = "Hello world Python"

result = re.findall("[A-Z][a-z]+", text)

print(result)

#5
import re

text = "a123b"

if re.fullmatch("a.*b", text):
    print("Match")
else:
    print("No match")

#^6
text = "Hello, world. Python"

result = re.sub("[ ,.]", ":", text)

print(result)

#7

text = "hello_world"

result = re.sub("_([a-z])", lambda x: x.group(1).upper(), text)

print(result)

#8
text = "HelloWorldPython"

result = re.findall("[A-Z][a-z]*", text)

print(result)

#9
text = "HelloWorldPython"

result = re.sub("([A-Z])", r" \1", text)

print(result.strip())

#10
text = "helloWorldPython"

result = re.sub("([A-Z])", r"_\1", text).lower()

print(result)
