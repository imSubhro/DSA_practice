class person:
    country = "India"

    def takeBreath(self): 
        print("I am breathing...")

class Employee(person):
    company = 'Honda'

    def __init__(self):
        super().__init__()        
        print("Intializing Employee...\n")

    def getSalary(self):
        print(f"Salary is {self.salary}")

    def takeBreath(self):
        super().takeBreath()
        print("I am an Employee so I am luckliy breathing++..")

class programmer(Employee):
    company = "Fiverr"

    def getSalary(self):
        print("No salary to programmers")

p = person()
p.takeBreath()

e = Employee()
pr = programmer()

pr = programmer()
pr.takeBreath()
