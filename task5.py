import csv
from pathlib import Path
from typing import Any


# 1. Calculate bonus using *args and **kwargs
def calculate_bonus(
    salary: float,
    rate: float = 0.1,
    *extras: float,
    **options: Any
) -> float:

    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# 2. Employee class
class Employee:

    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    def get_details(self) -> str:
        return f"Name: {self.name}, Salary: {self.salary}"

    @property
    def annual_salary(self) -> float:
        return self.salary * 12


# 3. Manager class inheriting Employee
class Manager(Employee):

    def __init__(
        self,
        name: str,
        salary: float,
        team_size: int
    ) -> None:

        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self) -> str:
        return (
            f"Name: {self.name}, "
            f"Salary: {self.salary}, "
            f"Team Size: {self.team_size}"
        )


# 4. Decorator
def log_call(func: Any) -> Any:

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# Apply decorator to Manager.get_details
Manager.get_details = log_call(Manager.get_details)


# 5. Read employees.csv using pathlib and csv
def read_employees() -> list[dict[str, str]]:
    employees = []

    file_path = Path(__file__).parent / "employees.csv"

    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            employees.append(row)

    return employees


# 6. Salary category using for loop and if/elif/else
def display_salary_categories(
    employees: list[dict[str, str]]
) -> None:

    for employee in employees:

        name = employee["name"]
        salary = int(employee["salary"])

        if salary < 50000:
            category = "Low Salary"

        elif salary < 70000:
            category = "Medium Salary"

        else:
            category = "High Salary"

        print(f"{name} - {category}")


# 7. Main function
def main() -> None:

    employees = read_employees()

    print("Salary Categories:")

    display_salary_categories(employees)

    # Bonus calculation
    bonus = calculate_bonus(
        50000,
        0.1,
        1000,
        2000,
        cap=7000
    )

    print("\nCalculated Bonus:", bonus)

    # Employee object
    employee = Employee("Arun", 30000)

    print("\nEmployee Details:")
    print(employee.get_details())
    print("Annual Salary:", employee.annual_salary)

    # Manager object
    manager = Manager("Rahul", 60000, 5)

    print("\nManager Details:")
    print(manager.get_details())


if __name__ == "__main__":
    main()