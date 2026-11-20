from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["company_db"]

employees = db["employees"]
departments = db["departments"]

# Clear old data for repeatable testing
employees.delete_many({})
departments.delete_many({})

# 1. Insert one employee
employees.insert_one({
    "emp_id": 1,
    "name": "Arun",
    "department": "IT",
    "salary": 50000,
    "dept_id": 101
})

print("One employee inserted successfully")

# 2. Insert multiple employees
employee_data = [
    {
        "emp_id": 2,
        "name": "Priya",
        "department": "IT",
        "salary": 60000,
        "dept_id": 101
    },
    {
        "emp_id": 3,
        "name": "Kumar",
        "department": "HR",
        "salary": 40000,
        "dept_id": 102
    },
    {
        "emp_id": 4,
        "name": "Divya",
        "department": "HR",
        "salary": 45000,
        "dept_id": 102
    },
    {
        "emp_id": 5,
        "name": "Ravi",
        "department": "Finance",
        "salary": 55000,
        "dept_id": 103
    }
]

employees.insert_many(employee_data)

print("Multiple employees inserted successfully")

# 3. Find employees in IT department
print("\nIT Department Employees:")

for emp in employees.find({"department": "IT"}):
    print(emp)

# 4. Update one employee salary
employees.update_one(
    {"emp_id": 1},
    {"$set": {"salary": 65000}}
)

print("\nSalary updated successfully")

# 5. Average salary per department
print("\nAverage Salary Per Department:")

pipeline = [
    {
        "$group": {
            "_id": "$department",
            "average_salary": {"$avg": "$salary"}
        }
    }
]

results = employees.aggregate(pipeline)

for result in results:
    print(result)

# 6. Insert departments
departments.insert_many([
    {"dept_id": 101, "dept_name": "Information Technology"},
    {"dept_id": 102, "dept_name": "Human Resources"},
    {"dept_id": 103, "dept_name": "Finance"}
])

# 7. Lookup employees with departments
print("\nEmployees Joined With Departments:")

lookup_pipeline = [
    {
        "$lookup": {
            "from": "departments",
            "localField": "dept_id",
            "foreignField": "dept_id",
            "as": "department_details"
        }
    }
]

joined_results = employees.aggregate(lookup_pipeline)

for result in joined_results:
    print(result)

client.close()
pipeline = [
    {
        "$match": {
            "salary": {"$gt": 0}
        }
    },
    {
        "$group": {
            "_id": "$department",
            "average_salary": {"$avg": "$salary"}
        }
    }
]

results = employees.aggregate(pipeline)

for result in results:
    print(result)