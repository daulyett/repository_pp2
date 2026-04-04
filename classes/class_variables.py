class Employee:
    company_name = "TechCorp"

    def __init__(self, name):
        self.name = name


emp1 = Employee("Alice")
emp2 = Employee("Bob")

print(emp1.company_name)
print(emp2.company_name)