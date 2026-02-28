import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1


a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R


if a == 0:
   
    print("0.0")
else:
    D = b*b - 4*a*c  

    if D < 0:
     
        if c <= 0:
           
            length = math.sqrt(a)
            print(f"{length:.10f}")
        else:
            print("0.0")
    else:
        sqrtD = math.sqrt(D)
        t1 = (-b - sqrtD) / (2*a)
        t2 = (-b + sqrtD) / (2*a)

        
        left = max(0.0, t1)
        right = min(1.0, t2)

        if right <= left:
            print("0.0")
        else:
            length = (right - left) * math.sqrt(a)
            print(f"{length:.10f}")