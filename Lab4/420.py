import math

def clamp(x, lo=-1.0, hi=1.0):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
seg_len = math.hypot(dx, dy)


d1 = math.hypot(x1, y1)
d2 = math.hypot(x2, y2)


if seg_len == 0:
    closest_dist = d1
else:
    t = - (x1 * dx + y1 * dy) / (dx * dx + dy * dy)  
    if t < 0:
        closest_dist = d1
    elif t > 1:
        closest_dist = d2
    else:
        px = x1 + t * dx
        py = y1 + t * dy
        closest_dist = math.hypot(px, py)


if closest_dist >= R - 1e-12:
    ans = seg_len
else:
    

    
    dot = x1 * x2 + y1 * y2
    cos_theta = clamp(dot / (d1 * d2))
    theta = math.acos(cos_theta)

    
    alpha = math.acos(clamp(R / d1))
    beta  = math.acos(clamp(R / d2))

   
    phi = theta - alpha - beta
    if phi < 0:
        phi = 0.0  

    
    tang1 = math.sqrt(max(0.0, d1 * d1 - R * R))
    tang2 = math.sqrt(max(0.0, d2 * d2 - R * R))

    ans = tang1 + tang2 + R * phi

print(f"{ans:.10f}")