n = int(input()) 


serials = {}


for _ in range(n):
    name, episodes = input().split()  
    episodes = int(episodes)  
    
    
    if name in serials:
        serials[name] += episodes
    else:
        serials[name] = episodes


sorted_serials = sorted(serials.items())


for name, episodes in sorted_serials:
    print(name, episodes)
