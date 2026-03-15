class person:
    country = "India"

    def takeBreath(self):
        print("I am breathing...")

class Employee(person):
    company = 'Honda'

    def getSalary(self):
        print(f"Salary is {self.salary}")


    def takeBreath(self):
        print("I am an Employee so I am luckliy breathing")

class programmer(Employee):
    company = "Fiverr"

    def getSalary(self):
        print("No salary to programmers")

p = person()
p.takeBreath()
e = Employee()
pr = programmer()
pr.takeBreath()
