import csv
import json

# 1. Write names to names.txt
names = ["Arun", "Priya", "Rahul", "Divya", "Karthik"]

with open("names.txt", "w") as file:
    for name in names:
        file.write(name + "\n")

# Read names with line numbers
print("Names:")
with open("names.txt", "r") as file:
    for number, name in enumerate(file, start=1):
        print(f"{number}. {name.strip()}")


# 2. Create students.csv
students = [
    {"name": "Arun", "marks": 55},
    {"name": "Priya", "marks": 60},
    {"name": "Rahul", "marks": 72},
    {"name": "Divya", "marks": 88},
    {"name": "Karthik", "marks": 45}
]

with open("students.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(students)

# Read CSV using DictReader
print("\nStudents with marks above 60:")
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    above_60 = []
    for student in reader:
        if int(student["marks"]) > 60:
            above_60.append(
                f'{student["name"]} {student["marks"]}'
            )

    print("Above 60:", " | ".join(above_60))


# 3. Save students to students.json
with open("students.json", "w") as file:
    json.dump(students, file, indent=2)

# Read JSON using json.load
print("\nStudents from JSON:")
with open("students.json", "r") as file:
    data = json.load(file)

    for student in data:
        print(student["name"], student["marks"])


# 4. Handle missing file
try:
    with open("missing.txt", "r") as file:
        content = file.read()
        print(content)

except FileNotFoundError:
    print("\nmissing.txt -> File not found")