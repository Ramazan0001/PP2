from __future__ import division
import sys

class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        Employee.__init__(self, name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100.0)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        Employee.__init__(self, name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500

class Intern(Employee):
    def __init__(self, name, base_salary):
        Employee.__init__(self, name, base_salary)

line = sys.stdin.readline().strip()
parts = line.split()

role = parts[0]

if role == "Manager":
    name = parts[1]
    base = int(parts[2])
    bonus = int(parts[3])
    emp = Manager(name, base, bonus)
elif role == "Developer":
    name = parts[1]
    base = int(parts[2])
    projects = int(parts[3])
    emp = Developer(name, base, projects)
else:
    name = parts[1]
    base = int(parts[2])
    emp = Intern(name, base)

sys.stdout.write("Name: {}, Total: {:.2f}\n".format(emp.name, emp.total_salary()))
