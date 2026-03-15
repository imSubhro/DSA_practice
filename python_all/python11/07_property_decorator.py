class Employee:
    company = "Bharat Gas"
    salary = 5600
    salarybouns = 400
   # totalSalary = 6100

    @property
    def totalSalary(self):
        return self.salary + self.salarybouns

    @totalSalary.setter
    def totalSalary(self,val):
        salarybouns = val - self.salary

e = Employee()
print(e.totalSalary)
e.totalSalary = 5800
print(e.salary)
print(e.salarybouns)

