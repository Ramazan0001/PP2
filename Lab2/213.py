x = int(input())  

if x <= 1:
    print("No")  
else:
    for i in range(2, x):  
        if x % i == 0:  
            print("No")
            break  
    else:
        print("Yes") 

