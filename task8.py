import csv

# 1. Calculate bonus function
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# 2. Employee class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"Name: {self.name}, Salary: {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# 3. Decorator
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# 4. Manager class (Inheritance)
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return (
            f"Manager: {self.name}, "
            f"Salary: {self.salary}, "
            f"Team Size: {self.team_size}"
        )


# 5. Read employees.csv
employees = []

with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        employees.append(
            Employee(row["name"], int(row["salary"]))
        )


# 6. Display employee details
print("EMPLOYEE DETAILS")

for emp in employees:
    print(emp.get_details())
    print("Annual Salary:", emp.annual_salary)
    print("Bonus:", calculate_bonus(emp.salary))
    print("-" * 40)


# 7. Test bonus with extras and cap
print("Bonus with extras:",
      calculate_bonus(50000, 0.1, 1000, 2000))

print("Bonus with cap:",
      calculate_bonus(50000, 0.1, 1000, 2000, cap=6000))


# 8. Create Manager object
manager = Manager("Arun", 100000, 5)

print("\nMANAGER DETAILS")
print(manager.get_details())
print("Annual Salary:", manager.annual_salary)
for emp in employees:
    name = emp["name"]
    salary = emp["salary"]

    if salary < 50000:
        print(name, "- Low Salary")

    elif salary < 70000:
        print(name, "- Medium Salary")

    else:
        print(name, "- High Salary")