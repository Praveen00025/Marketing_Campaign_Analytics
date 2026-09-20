# ============================================================
# MARKETING CAMPAIGN ANALYTICS
# Project: Marketing Campaign Performance & ROI Analysis
# Dataset: 45.csv
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "45.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("MARKETING CAMPAIGN ANALYTICS")
print("=" * 70)

# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\n[1] Loading dataset...")

if not DATA_FILE.exists():
    print("ERROR: 45.csv was not found!")
    print(f"Expected location: {DATA_FILE}")
    exit()

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

# ============================================================
# 3. BASIC DATA INFORMATION
# ============================================================

print("\n[2] Dataset Information")
print("-" * 70)

print("\nColumns:")
for column in df.columns:
    print(f"- {column}")

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Rows:")
print(df.head())

# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

# ============================================================
# 5. CLEAN NUMERIC DATA
# ============================================================

print("\n[3] Cleaning numeric columns...")

# Remove $ and commas from Acquisition Cost
df["Acquisition_Cost"] = (
    df["Acquisition_Cost"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Acquisition_Cost"] = pd.to_numeric(
    df["Acquisition_Cost"],
    errors="coerce"
)

# Convert important numeric columns
numeric_columns = [
    "Conversion_Rate",
    "ROI",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "Acquisition_Cost"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\n[4] Missing Value Analysis")
print("-" * 70)

missing_values = df.isnull().sum()

missing_report = pd.DataFrame({
    "Column": missing_values.index,
    "Missing_Values": missing_values.values,
    "Missing_Percentage": (
        missing_values.values / len(df) * 100
    ).round(2)
})

print(missing_report)

missing_report.to_csv(
    OUTPUT_DIR / "missing_values_report.csv",
    index=False
)

# ============================================================
# 7. CHECK DUPLICATES
# ============================================================

print("\n[5] Duplicate Analysis")
print("-" * 70)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")

# ============================================================
# 8. CALCULATE DERIVED METRICS
# ============================================================

print("\n[6] Creating calculated metrics...")
print("-" * 70)

# ------------------------------------------------------------
# Total Conversions
# ------------------------------------------------------------
# Conversion_Rate is represented as decimal.
# Example: 0.04 = 4%

df["Total Conversions"] = (
    df["Clicks"] * df["Conversion_Rate"]
).round(0)

# ------------------------------------------------------------
# Engagement Rate
# ------------------------------------------------------------

df["Engagement Rate"] = (
    df["Engagement_Score"] / 10
).round(4)

# ------------------------------------------------------------
# Cost Per Click
# ------------------------------------------------------------

df["Cost Per Click (CPC)"] = np.where(
    df["Clicks"] > 0,
    df["Acquisition_Cost"] / df["Clicks"],
    0
)

df["Cost Per Click (CPC)"] = (
    df["Cost Per Click (CPC)"].round(2)
)

# ------------------------------------------------------------
# Cost Per Acquisition
# ------------------------------------------------------------

df["Cost Per Acquisition"] = np.where(
    df["Total Conversions"] > 0,
    df["Acquisition_Cost"] / df["Total Conversions"],
    0
)

df["Cost Per Acquisition"] = (
    df["Cost Per Acquisition"].round(2)
)

# ------------------------------------------------------------
# Total Acquisition Cost
# ------------------------------------------------------------

df["Total Acquisition Cost"] = df["Acquisition_Cost"]

# ------------------------------------------------------------
# Average Conversion Rate
# ------------------------------------------------------------

average_conversion_rate = df["Conversion_Rate"].mean()

df["Average Conversion Rate"] = average_conversion_rate

print("Calculated metrics created successfully.")

# ============================================================
# 9. BASIC STATISTICS
# ============================================================

print("\n[7] Statistical Summary")
print("-" * 70)

statistics = df[
    [
        "Conversion_Rate",
        "Acquisition_Cost",
        "ROI",
        "Clicks",
        "Impressions",
        "Engagement_Score",
        "Total Conversions",
        "Cost Per Click (CPC)",
        "Cost Per Acquisition"
    ]
].describe()

print(statistics)

statistics.to_csv(
    OUTPUT_DIR / "statistical_summary.csv"
)

# ============================================================
# 10. KEY BUSINESS METRICS
# ============================================================

print("\n[8] KEY BUSINESS METRICS")
print("=" * 70)

total_campaigns = len(df)
total_clicks = df["Clicks"].sum()
total_impressions = df["Impressions"].sum()
total_spend = df["Acquisition_Cost"].sum()
average_roi = df["ROI"].mean()
average_conversion = df["Conversion_Rate"].mean()
total_conversions = df["Total Conversions"].sum()
average_engagement = df["Engagement_Score"].mean()

print(f"Total Campaigns        : {total_campaigns:,}")
print(f"Total Impressions      : {total_impressions:,.0f}")
print(f"Total Clicks           : {total_clicks:,.0f}")
print(f"Total Acquisition Cost : ${total_spend:,.2f}")
print(f"Average ROI            : {average_roi:.2f}")
print(f"Average Conversion     : {average_conversion:.2%}")
print(f"Total Conversions      : {total_conversions:,.0f}")
print(f"Average Engagement     : {average_engagement:.2f}")

# ============================================================
# 11. COMPANY ANALYSIS
# ============================================================

print("\n[9] COMPANY PERFORMANCE")
print("-" * 70)

company_analysis = (
    df.groupby("Company")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum"),
        Total_Cost=("Acquisition_Cost", "sum"),
        Average_Engagement=("Engagement_Score", "mean")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(company_analysis)

company_analysis.to_csv(
    OUTPUT_DIR / "company_performance.csv"
)

# ============================================================
# 12. CAMPAIGN TYPE ANALYSIS
# ============================================================

print("\n[10] CAMPAIGN TYPE PERFORMANCE")
print("-" * 70)

campaign_analysis = (
    df.groupby("Campaign_Type")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum"),
        Total_Cost=("Acquisition_Cost", "sum"),
        Average_Engagement=("Engagement_Score", "mean")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(campaign_analysis)

campaign_analysis.to_csv(
    OUTPUT_DIR / "campaign_type_performance.csv"
)

# ============================================================
# 13. CHANNEL ANALYSIS
# ============================================================

print("\n[11] CHANNEL PERFORMANCE")
print("-" * 70)

channel_analysis = (
    df.groupby("Channel_Used")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum"),
        Total_Cost=("Acquisition_Cost", "sum")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(channel_analysis)

channel_analysis.to_csv(
    OUTPUT_DIR / "channel_performance.csv"
)

# ============================================================
# 14. LOCATION ANALYSIS
# ============================================================

print("\n[12] LOCATION PERFORMANCE")
print("-" * 70)

location_analysis = (
    df.groupby("Location")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(location_analysis)

location_analysis.to_csv(
    OUTPUT_DIR / "location_performance.csv"
)

# ============================================================
# 15. CUSTOMER SEGMENT ANALYSIS
# ============================================================

print("\n[13] CUSTOMER SEGMENT PERFORMANCE")
print("-" * 70)

segment_analysis = (
    df.groupby("Customer_Segment")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(segment_analysis)

segment_analysis.to_csv(
    OUTPUT_DIR / "customer_segment_performance.csv"
)

# ============================================================
# 16. SAVE CLEANED DATA
# ============================================================

print("\n[14] Saving cleaned dataset...")

df.to_csv(
    OUTPUT_DIR / "cleaned_marketing_campaign_data.csv",
    index=False
)

print("Cleaned dataset saved.")

# ============================================================
# 17. VISUALIZATION SETTINGS
# ============================================================

sns.set_theme(style="whitegrid")

# ============================================================
# 18. CHART 1 - ROI BY CAMPAIGN TYPE
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=campaign_analysis.reset_index(),
    x="Campaign_Type",
    y="Average_ROI"
)

plt.title("Average ROI by Campaign Type")
plt.xlabel("Campaign Type")
plt.ylabel("Average ROI")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "01_roi_by_campaign_type.png",
    dpi=300
)

plt.close()

# ============================================================
# 19. CHART 2 - ROI BY CHANNEL
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=channel_analysis.reset_index(),
    x="Channel_Used",
    y="Average_ROI"
)

plt.title("Average ROI by Marketing Channel")
plt.xlabel("Channel")
plt.ylabel("Average ROI")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "02_roi_by_channel.png",
    dpi=300
)

plt.close()

# ============================================================
# 20. CHART 3 - CONVERSION RATE BY CAMPAIGN TYPE
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=campaign_analysis.reset_index(),
    x="Campaign_Type",
    y="Average_Conversion"
)

plt.title("Average Conversion Rate by Campaign Type")
plt.xlabel("Campaign Type")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "03_conversion_by_campaign_type.png",
    dpi=300
)

plt.close()

# ============================================================
# 21. CHART 4 - ACQUISITION COST VS ROI
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df.sample(min(10000, len(df))),
    x="Acquisition_Cost",
    y="ROI",
    alpha=0.5
)

plt.title("Acquisition Cost vs ROI")
plt.xlabel("Acquisition Cost ($)")
plt.ylabel("ROI")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "04_acquisition_cost_vs_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 22. CHART 5 - CLICKS VS CONVERSIONS
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df.sample(min(10000, len(df))),
    x="Clicks",
    y="Total Conversions",
    alpha=0.5
)

plt.title("Clicks vs Total Conversions")
plt.xlabel("Clicks")
plt.ylabel("Total Conversions")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "05_clicks_vs_conversions.png",
    dpi=300
)

plt.close()

# ============================================================
# 23. CHART 6 - ROI DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="ROI",
    bins=30,
    kde=True
)

plt.title("ROI Distribution")
plt.xlabel("ROI")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "06_roi_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 24. CHART 7 - CONVERSION RATE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="Conversion_Rate",
    bins=30,
    kde=True
)

plt.title("Conversion Rate Distribution")
plt.xlabel("Conversion Rate")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "07_conversion_rate_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 25. CHART 8 - ENGAGEMENT SCORE
# ============================================================

engagement_data = (
    df["Engagement_Score"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=engagement_data.index,
    y=engagement_data.values
)

plt.title("Engagement Score Distribution")
plt.xlabel("Engagement Score")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "08_engagement_score_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 26. CHART 9 - TOP COMPANIES BY ROI
# ============================================================

top_companies = (
    company_analysis
    .sort_values("Average_ROI", ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_companies,
    x="Average_ROI",
    y="Company"
)

plt.title("Top 10 Companies by Average ROI")
plt.xlabel("Average ROI")
plt.ylabel("Company")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "09_top_10_companies_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 27. CHART 10 - TOP LOCATIONS BY ROI
# ============================================================

top_locations = (
    location_analysis
    .sort_values("Average_ROI", ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_locations,
    x="Average_ROI",
    y="Location"
)

plt.title("Top 10 Locations by Average ROI")
plt.xlabel("Average ROI")
plt.ylabel("Location")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "10_top_locations_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 28. CORRELATION ANALYSIS
# ============================================================

print("\n[15] Correlation Analysis")
print("-" * 70)

correlation_columns = [
    "Conversion_Rate",
    "Acquisition_Cost",
    "ROI",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "Total Conversions",
    "Cost Per Click (CPC)",
    "Cost Per Acquisition"
]

correlation_matrix = df[correlation_columns].corr()

print(correlation_matrix.round(2))

correlation_matrix.to_csv(
    OUTPUT_DIR / "correlation_matrix.csv"
)

# ============================================================
# 29. CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(12, 9))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Marketing Campaign Correlation Matrix")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "11_correlation_heatmap.png",
    dpi=300
)

plt.close()

# ============================================================
# 30. MONTHLY PERFORMANCE
# ============================================================

print("\n[16] Monthly Performance")

df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_analysis = (
    df.groupby("Year_Month")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Total Conversions", "sum"),
        Total_Cost=("Acquisition_Cost", "sum")
    )
    .reset_index()
)

print(monthly_analysis.head())

monthly_analysis.to_csv(
    OUTPUT_DIR / "monthly_performance.csv",
    index=False
)

# ============================================================
# 31. MONTHLY ROI CHART
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_analysis["Year_Month"],
    monthly_analysis["Average_ROI"],
    marker="o"
)

plt.title("Monthly Average ROI")
plt.xlabel("Month")
plt.ylabel("Average ROI")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "12_monthly_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 32. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nOutput folder:")
print(OUTPUT_DIR)

print("\nFiles generated:")

for file in sorted(OUTPUT_DIR.iterdir()):
    print(f" - {file.name}")

print("\n" + "=" * 70)
print("Marketing Campaign Analysis Finished!")
print("=" * 70)
