import csv
import json
import logging
import sys

from pathlib import Path
from typing import List, Optional, Union

import fitz
from openpyxl import Workbook, load_workbook



logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
EMPLOYEES: List[dict] = []



def read_employees(path: Path) -> List[dict]:
    employees: List[dict] = []

    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["salary"] = int(row["salary"])
                row["age"] = int(row["age"])
                employees.append(row)

    except FileNotFoundError:
        logger.error("Employee CSV file not found: %s", path)

    return employees



def write_json(employees: List[dict], path: Path) -> None:
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(employees, file, indent=4)

    except OSError as error:
        logger.error("Error writing JSON: %s", error)



def write_high_earners(
    employees: List[dict],
    path: Path
) -> int:

    high_earners = [
        employee for employee in employees
        if employee["salary"] > 50000
    ]

    try:
        if employees:
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=employees[0].keys()
                )

                writer.writeheader()
                writer.writerows(high_earners)

    except OSError as error:
        logger.error("Error writing high earners CSV: %s", error)
        return 0

    return len(high_earners)



def create_excel(employees: List[dict], path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employee Salaries"

    sheet.append(["Name", "Department", "Salary"])

    for employee in employees:
        sheet.append([
            employee["name"],
            employee["department"],
            employee["salary"]
        ])

    workbook.save(path)



def read_excel(path: Path) -> List[dict]:
    employees: List[dict] = []

    try:
        workbook = load_workbook(path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            employees.append({
                "name": row[0],
                "department": row[1],
                "salary": row[2]
            })

        workbook.close()

    except (FileNotFoundError, OSError) as error:
        logger.error("Excel reading error: %s", error)

    return employees



def extract_pdf(path: Path) -> str:
    try:
        with fitz.open(path) as document:
            if len(document) > 0:
                text = document[0].get_text()
                return text[:100]

    except (FileNotFoundError, RuntimeError) as error:
        logger.error("PDF extraction error: %s", error)

    return ""



def read_file(path: Union[str, Path]) -> Optional[dict]:
    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

            logger.error("JSON file must contain an object: %s", path)

    except FileNotFoundError:
        logger.error("File not found: %s", path)

    except json.JSONDecodeError as error:
        logger.error("Invalid JSON: %s", error)

    return None

def find_employee(name: str) -> Optional[dict]:
    for employee in EMPLOYEES:
        if employee["name"].lower() == name.lower():
            return employee

    return None



def main() -> None:
    global EMPLOYEES

    csv_path = BASE_DIR / "employees.csv"
    json_path = BASE_DIR / "employees.json"
    high_earners_path = BASE_DIR / "high_earners.csv"
    excel_path = BASE_DIR / "salary.xlsx"

    # Read CSV
    EMPLOYEES = read_employees(csv_path)

    # Write JSON
    write_json(EMPLOYEES, json_path)

    # Write high earners CSV
    high_count = write_high_earners(
        EMPLOYEES,
        high_earners_path
    )
    create_excel(EMPLOYEES, excel_path)

    # Read Excel back
    excel_data = read_excel(excel_path)

    # Read JSON back
    json_data = read_file(json_path)

    # Find employee
    employee = find_employee("Alice")

    # PDF extraction (optional command-line argument)
    pdf_text = ""

    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
        pdf_text = extract_pdf(pdf_path)
    else:
        pdf_files = sorted(BASE_DIR.glob("*.pdf"))

        if pdf_files:
            pdf_text = extract_pdf(pdf_files[0])

    # Required output
    print(
        f"Rows read: {len(EMPLOYEES)} | "
        f"High earners written: {high_count}"
    )

    logger.info("JSON records loaded: %s", len(json_data or {}))
    logger.info("Excel records read: %s", len(excel_data))
    logger.info("Employee found: %s", employee is not None)

    if pdf_text:
        logger.info("PDF first 100 characters: %s", pdf_text)


if __name__ == "__main__":
    main()
