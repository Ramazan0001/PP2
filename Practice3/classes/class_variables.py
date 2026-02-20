class student:
    school = "KBTU"

    def __init__(self,name):
        self.name = name
    
s1=student("Ramazan")
s2=student("Ali")
print(s1.name,s1.school)
print(s2.name,s2.school)