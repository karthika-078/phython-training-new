import pandas as pd
import numpy as np

# Step 1: Create employees.csv file
data = """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai
"""

with open("employees.csv", "w") as file:
    file.write(data)

# Step 2: Load CSV file
df = pd.read_csv("employees.csv")

print("Employee Data:")
print(df)

# Step 3: Basic DataFrame functions
print("\nFirst 5 rows:")
print(df.head())

print("\nDataFrame Information:")
df.info()

print("\nStatistical Description:")
print(df.describe())

# Step 4: Select columns
print("\nName Column:")
print(df["name"])

print("\nName and Salary Columns:")
print(df[["name", "salary"]])

# Step 5: Using loc
print("\nNames of Chennai Employees:")
chennai = df.loc[df["city"] == "Chennai", "name"]
print(", ".join(chennai))

# Step 6: Using iloc
print("\nFirst 3 Rows and Columns 2 to 3:")
print(df.iloc[0:3, 1:3])

# Step 7: Filtering employees
salary_filter = df[df["salary"] > 50000]

print("\nEmployees with Salary Above 50000:")
print(salary_filter)
print("Salary above 50000:", len(salary_filter), "employees")

# IT Department employees
it_employees = df[df["department"] == "IT"]

print("\nIT Department Employees:")
print(", ".join(it_employees["name"]))
print("IT department:", len(it_employees), "employees")

# Bonus Challenge: NumPy reshape
arr = np.arange(1, 25)

reshaped = arr.reshape(2, 3, 4)

print("\nReshaped 3D Array (2x3x4):")
print(reshaped)