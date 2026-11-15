
import csv
import json
import logging

from pathlib import Path
from typing import List, Optional, Union

from openpyxl import Workbook, load_workbook
import fitz  # PyMuPDF


# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# 1. Read employees.csv using pathlib and csv.DictReader
def read_employees(path: Union[str, Path]) -> List[dict]:

    file_path = Path(path)
    employees: List[dict] = []

    with file_path.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["salary"] = int(row["salary"])
            employees.append(row)

    return employees


# 2. Write employees.json
def write_json(employees: List[dict],
               path: Union[str, Path]) -> None:

    with Path(path).open("w") as file:
        json.dump(employees, file, indent=4)


# 3. Write high_earners.csv
def write_high_earners(employees: List[dict],
                       path: Union[str, Path]) -> int:

    high_earners = [
        emp for emp in employees
        if emp["salary"] > 50000
    ]

    with Path(path).open("w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["name", "department", "salary"]
        )

        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


# 4. Create Excel file using openpyxl
def create_excel(employees: List[dict],
                 path: Union[str, Path]) -> int:

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employee Salaries"

    sheet.append(["Name", "Department", "Salary"])

    for emp in employees:
        sheet.append([
            emp["name"],
            emp["department"],
            emp["salary"]
        ])

    workbook.save(path)

    return len(employees)


# 5. Read Excel file back
def read_excel(path: Union[str, Path]) -> List[dict]:

    workbook = load_workbook(path)
    sheet = workbook.active

    rows = list(sheet.iter_rows(values_only=True))

    headers = rows[0]

    employees = [
        dict(zip(headers, row))
        for row in rows[1:]
    ]

    return employees


# 6. Extract first page text from PDF
def extract_pdf_text(path: Union[str, Path]) -> str:

    document = fitz.open(path)

    try:
        if len(document) == 0:
            return ""

        page = document[0]
        text = page.get_text()

        return text[:100]

    finally:
        document.close()


# 7. Read JSON file with exception handling
def read_file(path: Union[str, Path]) -> Optional[dict]:

    try:
        with Path(path).open("r") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

            logger.error("Invalid JSON structure: expected an object")
            return None

    except FileNotFoundError:
        logger.error("File not found: %s", path)
        return None

    except json.JSONDecodeError:
        logger.error("Invalid JSON file: %s", path)
        return None


# 8. Find employee by name
def find_employee(name: str) -> Optional[dict]:

    employees = read_employees("employees.csv")

    for emp in employees:
        if emp["name"].lower() == name.lower():
            return emp

    return None


# 9. Function demonstrating Union[int, str]
def get_salary_category(salary: Union[int, str]) -> str:

    salary = int(salary)

    if salary < 50000:
        return "Low Salary"

    elif salary < 70000:
        return "Medium Salary"

    else:
        return "High Salary"


# 10. Main program
def main() -> None:

    # Read CSV
    employees = read_employees("employees.csv")

    # Write JSON
    write_json(employees, "employees.json")

    # Write high earners CSV
    count = write_high_earners(
        employees,
        "high_earners.csv"
    )

    print(
        f"Rows read: {len(employees)} | "
        f"High earners written: {count}"
    )

    # Create Excel
    create_excel(employees, "salary.xlsx")

    # Read Excel back
    excel_data = read_excel("salary.xlsx")

    print(
        f"salary.xlsx created and read back: "
        f"{len(excel_data)} rows"
    )

    # Find employee
    employee = find_employee("Rahul")

    if employee:
        print("Employee found:", employee)

    # Salary categories
    for emp in employees:
        print(
            emp["name"],
            "-",
            get_salary_category(emp["salary"])
        )

    # Read missing file (demonstrate exception handling)
    read_file("missing.txt")

    # Extract PDF text if sample.pdf exists
    pdf_path = Path("sample.pdf")

    if pdf_path.exists():
        pdf_text = extract_pdf_text(pdf_path)
        print("PDF first 100 characters:", pdf_text)


if __name__ == "__main__":
    main()
