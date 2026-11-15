
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    'Employee': ['Arun', 'Priya', 'Rahul', 'Sneha', 'Kumar',
                 'Divya', 'Ajay', 'Meena', 'Vijay', 'Anu'],

    'Department': ['IT', 'HR', 'IT', 'Finance', 'HR',
                   'Finance', 'IT', 'HR', 'Finance', 'IT'],

    'City': ['Chennai', 'Mumbai', 'Chennai', 'Delhi', 'Mumbai',
             'Delhi', 'Chennai', 'Mumbai', 'Delhi', 'Chennai'],

    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male',
               'Female', 'Male', 'Female', 'Male', 'Female'],

    'Salary': [50000, 40000, 60000, 55000, 45000,
               65000, 70000, 42000, 58000, 52000],

    'Age': [25, 28, 30, 35, 27, 32, 29, 26, 34, 31],

    'Experience': [2, 4, 5, 8, 3, 7, 6, 2, 9, 5],

    'Performance': [80, 75, 90, 85, 78, 88, 95, 76, 89, 84]
}

df = pd.DataFrame(data)

print("EMPLOYEE DATASET")
print(df)

numeric_cols = ['Salary', 'Age', 'Experience', 'Performance']

summary = df[numeric_cols].agg(
    ['mean', 'median', 'min', 'max', 'std']
)

print("\nSUMMARY STATISTICS")
print(summary)


# ============================================
# 4. Groupby and Aggregation
# ============================================

# A. Department-wise analysis

dept_summary = df.groupby('Department').agg(
    Average_Salary=('Salary', 'mean'),
    Total_Salary=('Salary', 'sum'),
    Employee_Count=('Employee', 'count'),
    Average_Performance=('Performance', 'mean')
)

print("\nDEPARTMENT-WISE ANALYSIS")
print(dept_summary)


# B. City-wise analysis

city_summary = df.groupby('City').agg(
    Average_Salary=('Salary', 'mean'),
    Employee_Count=('Employee', 'count')
)

print("\nCITY-WISE ANALYSIS")
print(city_summary)


# C. Gender-wise analysis

gender_summary = df.groupby('Gender').agg(
    Average_Salary=('Salary', 'mean'),
    Average_Performance=('Performance', 'mean'),
    Employee_Count=('Employee', 'count')
)

print("\nGENDER-WISE ANALYSIS")
print(gender_summary)


# ============================================
# 5. Correlation Analysis
# ============================================

corr_matrix = df[numeric_cols].corr()

print("\nCORRELATION MATRIX")
print(corr_matrix)


# Correlation Heatmap

plt.figure(figsize=(8, 5))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap='coolwarm',
    fmt='.2f'
)

plt.title("Employee Data Correlation")
plt.tight_layout()
plt.show()


# Find Top 3 Correlations

corr_pairs = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
).stack()

top_3 = corr_pairs.reindex(
    corr_pairs.abs().sort_values(ascending=False).index
).head(3)

print("\nTOP 3 CORRELATION RELATIONSHIPS")

for (col1, col2), value in top_3.items():
    print(f"{col1} vs {col2}: {value:.3f}")
print("\nQUESTION 1: Highest Average Salary Department")

result1 = df.groupby('Department')['Salary'].mean()

print(result1)

print("Answer:", result1.idxmax(),
      "with average salary:", result1.max())


# Question 2:
# Which city has the highest number of employees?

print("\nQUESTION 2: City with Highest Employees")

result2 = df.groupby('City')['Employee'].count()

print(result2)

print("Answer:", result2.idxmax(),
      "with", result2.max(), "employees")


# Question 3:
# Which gender has the highest average salary?

print("\nQUESTION 3: Gender with Highest Average Salary")

result3 = df.groupby('Gender')['Salary'].mean()

print(result3)

print("Answer:", result3.idxmax(),
      "with average salary:", result3.max())


# Question 4:
# Does experience affect salary?

print("\nQUESTION 4: Experience and Salary Relationship")

result4 = df['Experience'].corr(df['Salary'])

print("Correlation:", round(result4, 3))

if result4 > 0.7:
    print("Answer: Strong positive relationship")
elif result4 > 0:
    print("Answer: Positive relationship")
elif result4 < 0:
    print("Answer: Negative relationship")
else:
    print("Answer: No linear relationship")


# Question 5:
# Which employee has the highest performance?

print("\nQUESTION 5: Highest Performance Employee")

best_employee = df.loc[df['Performance'].idxmax()]

print("Employee:", best_employee['Employee'])
print("Performance Score:", best_employee['Performance'])


# ============================================
# 7. Create Department Budget Dataset
# ============================================

budget_data = {
    'Department': ['IT', 'HR', 'Finance'],
    'Budget': [300000, 200000, 250000]
}

budget_df = pd.DataFrame(budget_data)

print("\nDEPARTMENT BUDGET TABLE")
print(budget_df)


# ============================================
# 8. Merge Two DataFrames
# ============================================

merged_df = pd.merge(
    df,
    budget_df,
    on='Department',
    how='left'
)

print("\nMERGED DATASET")
print(merged_df)


# ============================================
# 9. Budget Analysis
# ============================================

budget_summary = merged_df.groupby('Department').agg(
    Total_Salary=('Salary', 'sum'),
    Budget=('Budget', 'first')
)

budget_summary['Remaining_Budget'] = (
    budget_summary['Budget'] - budget_summary['Total_Salary']
)

print("\nDEPARTMENT BUDGET ANALYSIS")
print(budget_summary)


# ============================================
# 10. Final Conclusion
# ============================================

print("\n========== FINAL CONCLUSION ==========")

print("1. Highest average salary department:",
      result1.idxmax(), "-", result1.max())

print("2. City with most employees:",
      result2.idxmax(), "-", result2.max(), "employees")

print("3. Gender with highest average salary:",
      result3.idxmax(), "-", result3.max())

print("4. Experience-Salary Correlation:",
      round(result4, 3))

print("5. Highest performing employee:",
      best_employee['Employee'], "-",
      best_employee['Performance'])

print("6. Department with highest remaining budget:",
      budget_summary['Remaining_Budget'].idxmax(),
      "-",
      budget_summary['Remaining_Budget'].max())

print("\nEDA ANALYSIS COMPLETED SUCCESSFULLY!")

