#1
def sq(x):
    return x*x
a = sq(6)
print(a)
#2
def name(first,last):
    return first +" "+last
print(name("Alimbek","Ramazan"))
#3
def minmax(a,b):
    if a < b:
        return a,b
    else:
        return b,a

mn,mx = minmax(9,12)
print(mn,mx)