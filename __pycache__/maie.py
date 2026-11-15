import pandas as pd
import numpy as np

# 1. Load original dataset
df = pd.read_csv("data.csv")

# Before cleaning summary
before_rows = len(df)
before_missing = int(df.isnull().sum().sum())
before_duplicates = int(df.duplicated().sum())

print("BEFORE CLEANING")
print("Rows:", before_rows)
print("Missing values:", before_missing)
print("Duplicates:", before_duplicates)


# 2. Remove duplicate rows
df = df.drop_duplicates().copy()


# 3. Standardise text values
text_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    df[col] = df[col].apply(
        lambda x: x.strip().title() if isinstance(x, str) else x
    )


# 4. Fix data types
# Detect date columns using their column names
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Convert columns containing numbers stored as text
for col in df.select_dtypes(include=["object", "string"]).columns:
    original = df[col]
    converted = pd.to_numeric(
        original.astype("string").str.replace(",", "", regex=False),
        errors="coerce"
    )

    non_missing = original.notna().sum()

    if non_missing > 0:
        success_ratio = converted.notna().sum() / non_missing

        if success_ratio >= 0.8:
            df[col] = converted


# 5. Handle missing values with a reason for each column
print("\nMISSING VALUE TREATMENT")

for col in list(df.columns):

    missing_count = df[col].isnull().sum()

    if missing_count == 0:
        print(f"{col}: No missing values")
        continue

    if df[col].isnull().all():
        df.drop(columns=[col], inplace=True)
        print(f"{col}: Dropped column because all values are missing")

    elif pd.api.types.is_numeric_dtype(df[col]):
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
        print(f"{col}: Filled {missing_count} missing values with median ({median_value})")

    else:
        mode_values = df[col].mode(dropna=True)

        if not mode_values.empty:
            mode_value = mode_values.iloc[0]
            df[col] = df[col].fillna(mode_value)
            print(f"{col}: Filled {missing_count} missing values with mode ({mode_value})")
        else:
            print(f"{col}: Left missing values and flagged for review")


# 6. Detect outliers using IQR
print("\nOUTLIER DETECTION")

numeric_columns = df.select_dtypes(include=np.number).columns

outlier_flags = pd.Series(False, index=df.index)

for col in numeric_columns:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = (df[col] < lower_limit) | (df[col] > upper_limit)

    outlier_count = int(outliers.sum())
    outlier_flags |= outliers

    print(f"{col}: {outlier_count} outliers detected")

# Keep original values but flag outlier rows
df["outlier_flag"] = outlier_flags


# 7. After cleaning summary
after_rows = len(df)
after_missing = int(df.isnull().sum().sum())
after_duplicates = int(df.duplicated().sum())

summary = pd.DataFrame({
    "Metric": ["Rows", "Missing values", "Duplicates"],
    "Before": [
        before_rows,
        before_missing,
        before_duplicates
    ],
    "After": [
        after_rows,
        after_missing,
        after_duplicates
    ]
})

print("\nBEFORE / AFTER SUMMARY")
print(summary.to_string(index=False))


# 8. Save cleaned dataset
df.to_csv("clean_data.csv", index=False)

print("\nCleaned dataset saved as clean_data.csv")
