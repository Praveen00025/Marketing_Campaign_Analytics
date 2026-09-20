import pandas as pd
from pathlib import Path

# ============================================================
# DATASET VALIDATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "45.csv"

print("=" * 70)
print("MARKETING CAMPAIGN DATASET VALIDATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load original dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("\n1. DATASET SIZE")
print("-" * 70)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

# ------------------------------------------------------------
# 2. Show every column
# ------------------------------------------------------------

print("\n2. ALL COLUMNS")
print("-" * 70)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

# ------------------------------------------------------------
# 3. Data types
# ------------------------------------------------------------

print("\n3. DATA TYPES")
print("-" * 70)

for column in df.columns:
    print(f"{column:<30} -> {df[column].dtype}")

# ------------------------------------------------------------
# 4. Missing values
# ------------------------------------------------------------

print("\n4. MISSING VALUES")
print("-" * 70)

missing = df.isnull().sum()

for column, value in missing.items():
    percentage = (value / len(df)) * 100
    print(f"{column:<30} -> {value:>8,} ({percentage:>6.2f}%)")

# ------------------------------------------------------------
# 5. Duplicate rows
# ------------------------------------------------------------

print("\n5. DUPLICATE ROWS")
print("-" * 70)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates:,}")

# ------------------------------------------------------------
# 6. Unique values
# ------------------------------------------------------------

print("\n6. UNIQUE VALUES")
print("-" * 70)

for column in df.columns:
    print(f"{column:<30} -> {df[column].nunique(dropna=True):,}")

# ------------------------------------------------------------
# 7. Numeric columns
# ------------------------------------------------------------

print("\n7. NUMERIC COLUMNS")
print("-" * 70)

numeric_columns = df.select_dtypes(
    include=["number"]
).columns

for column in numeric_columns:
    print(f"- {column}")

# ------------------------------------------------------------
# 8. Categorical columns
# ------------------------------------------------------------

print("\n8. CATEGORICAL / TEXT COLUMNS")
print("-" * 70)

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:
    print(f"- {column}")

# ------------------------------------------------------------
# 9. First 5 rows
# ------------------------------------------------------------

print("\n9. FIRST 5 ROWS")
print("-" * 70)

print(df.head().to_string())

# ------------------------------------------------------------
# 10. Last 5 rows
# ------------------------------------------------------------

print("\n10. LAST 5 ROWS")
print("-" * 70)

print(df.tail().to_string())

# ------------------------------------------------------------
# 11. Statistical summary
# ------------------------------------------------------------

print("\n11. NUMERIC SUMMARY")
print("-" * 70)

print(
    df.describe(include="all").transpose().to_string()
)

# ------------------------------------------------------------
# 12. Check required original columns
# ------------------------------------------------------------

expected_columns = [
    "Campaign_ID",
    "Company",
    "Campaign_Type",
    "Target_Audience",
    "Duration",
    "Channel_Used",
    "Conversion_Rate",
    "Acquisition_Cost",
    "ROI",
    "Location",
    "Language",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "Customer_Segment",
    "Date",
    "Average Conversion Rate",
    "Engagement Rate",
    "Total Acquisition Cost",
    "Cost Per Click (CPC)",
    "Cost Per Acquisition",
    "Total Conversions"
]

print("\n12. COLUMN VALIDATION")
print("-" * 70)

missing_columns = [
    column for column in expected_columns
    if column not in df.columns
]

extra_columns = [
    column for column in df.columns
    if column not in expected_columns
]

if not missing_columns:
    print("All expected columns are present. ✅")
else:
    print("Missing columns:")
    for column in missing_columns:
        print(f"- {column}")

if extra_columns:
    print("\nAdditional columns:")
    for column in extra_columns:
        print(f"- {column}")
else:
    print("No unexpected columns found. ✅")

# ------------------------------------------------------------
# 13. Final validation
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

print(f"Original rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")

if len(df.columns) == 22:
    print("22-column structure confirmed. ✅")
else:
    print("WARNING: Column count is different from expected 22. ⚠️")

print("=" * 70)