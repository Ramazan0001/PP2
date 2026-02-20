n = int(input())  
num = list(map(int, input().split()))  

freq = {}


for x in num:
    if x in freq:
        freq[x] += 1  
    else:
        freq[x] = 1   


max_freq = max(freq.values())


most_frequent_elements = [key for key, value in freq.items() if value == max_freq]


print(min(most_frequent_elements))
