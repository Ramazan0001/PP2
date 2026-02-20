def func(a):
    count1 = 0 
    count2 = 0
    while a > 0:
        if a % 2 == 1:
            count1+=1
        else:
            count2+=1
            

        a //= 10
    print(count1,count2)

    
a = int(input())
func(a)


