n = int(input())  
strings = [input().strip() for _ in range(n)]  

indexed_strings = [(strings[i], i + 1) for i in range(n)]


indexed_strings.sort(key=lambda x: x[0])  


for s, index in indexed_strings:
    print(s, index)
