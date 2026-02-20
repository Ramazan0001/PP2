class A:
    def show1(self):
        print("A")
class B:
    def show2(self):
        print("B")
class C(A,B):
    pass


c= C()
c.show1()
c.show2()

     