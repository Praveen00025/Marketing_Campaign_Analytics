# ============================================================
# MARKETING CAMPAIGN ANALYTICS
# EXPLORATORY DATA ANALYSIS (EDA)
#
# Original Dataset:
# 200,000 rows
# 22 columns
#
# IMPORTANT:
# The original 22 columns are NOT deleted or overwritten.
# Derived metrics are created separately for analysis.
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "45.csv"
EDA_DIR = PROJECT_DIR / "eda_output"

EDA_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("MARKETING CAMPAIGN ANALYTICS - EDA")
print("=" * 80)

# ============================================================
# 2. LOAD ORIGINAL DATA
# ============================================================

print("\n[1] Loading original dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# 3. STORE ORIGINAL COLUMN LIST
# ============================================================

original_columns = df.columns.tolist()

print("\n[2] ORIGINAL COLUMNS")
print("-" * 80)

for i, column in enumerate(original_columns, 1):
    print(f"{i:02}. {column}")

# ============================================================
# 4. BASIC DATASET INFORMATION
# ============================================================

print("\n[3] DATASET INFORMATION")
print("-" * 80)

print(f"Number of rows    : {df.shape[0]:,}")
print(f"Number of columns : {df.shape[1]:,}")
print(f"Memory usage      : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ============================================================
# 5. DATA TYPES
# ============================================================

print("\n[4] DATA TYPES")
print("-" * 80)

data_types = pd.DataFrame({
    "Column": df.columns,
    "Data_Type": df.dtypes.astype(str).values
})

print(data_types.to_string(index=False))

data_types.to_csv(
    EDA_DIR / "01_data_types.csv",
    index=False
)

# ============================================================
# 6. MISSING VALUE ANALYSIS
# ============================================================

print("\n[5] MISSING VALUE ANALYSIS")
print("-" * 80)

missing_count = df.isnull().sum()

missing_percentage = (
    missing_count / len(df) * 100
).round(2)

missing_report = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": missing_count.values,
    "Missing_Percentage": missing_percentage.values
})

print(missing_report.to_string(index=False))

missing_report.to_csv(
    EDA_DIR / "02_missing_values.csv",
    index=False
)

# ============================================================
# 7. DUPLICATE ANALYSIS
# ============================================================

print("\n[6] DUPLICATE ANALYSIS")
print("-" * 80)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")

duplicate_report = pd.DataFrame({
    "Metric": ["Duplicate Rows"],
    "Count": [duplicate_count]
})

duplicate_report.to_csv(
    EDA_DIR / "03_duplicates.csv",
    index=False
)

# ============================================================
# 8. UNIQUE VALUES FOR EVERY COLUMN
# ============================================================

print("\n[7] UNIQUE VALUE ANALYSIS")
print("-" * 80)

unique_report = pd.DataFrame({
    "Column": df.columns,
    "Unique_Values": [
        df[column].nunique(dropna=True)
        for column in df.columns
    ]
})

print(unique_report.to_string(index=False))

unique_report.to_csv(
    EDA_DIR / "04_unique_values.csv",
    index=False
)

# ============================================================
# 9. FIRST 10 ROWS
# ============================================================

print("\n[8] FIRST 10 ROWS")
print("-" * 80)

print(df.head(10).to_string())

df.head(10).to_csv(
    EDA_DIR / "05_first_10_rows.csv",
    index=False
)

# ============================================================
# 10. LAST 10 ROWS
# ============================================================

print("\n[9] LAST 10 ROWS")
print("-" * 80)

print(df.tail(10).to_string())

df.tail(10).to_csv(
    EDA_DIR / "06_last_10_rows.csv",
    index=False
)

# ============================================================
# 11. NUMERIC SUMMARY
# ============================================================

print("\n[10] NUMERIC SUMMARY")
print("-" * 80)

numeric_columns_original = df.select_dtypes(
    include=np.number
).columns.tolist()

numeric_summary = df[numeric_columns_original].describe().T

print(numeric_summary.to_string())

numeric_summary.to_csv(
    EDA_DIR / "07_numeric_summary.csv"
)

# ============================================================
# 12. CATEGORICAL SUMMARY
# ============================================================

print("\n[11] CATEGORICAL COLUMNS")
print("-" * 80)

categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

for column in categorical_columns:
    print(
        f"{column:<25} "
        f"Unique values: {df[column].nunique(dropna=True):,}"
    )

categorical_summary = pd.DataFrame({
    "Column": categorical_columns,
    "Unique_Values": [
        df[column].nunique(dropna=True)
        for column in categorical_columns
    ]
})

categorical_summary.to_csv(
    EDA_DIR / "08_categorical_summary.csv",
    index=False
)

# ============================================================
# 13. CLEAN NUMERIC COPY FOR ANALYSIS
#
# IMPORTANT:
# This does NOT modify the original df.
# ============================================================

analysis_df = df.copy()

# Acquisition cost contains "$" and commas
analysis_df["Acquisition_Cost_Clean"] = (
    analysis_df["Acquisition_Cost"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

analysis_df["Acquisition_Cost_Clean"] = pd.to_numeric(
    analysis_df["Acquisition_Cost_Clean"],
    errors="coerce"
)

# ============================================================
# 14. CONVERT DATE
# ============================================================

analysis_df["Date_Clean"] = pd.to_datetime(
    analysis_df["Date"],
    errors="coerce"
)

print("\n[12] DATE ANALYSIS")
print("-" * 80)

print(
    f"Minimum Date: "
    f"{analysis_df['Date_Clean'].min()}"
)

print(
    f"Maximum Date: "
    f"{analysis_df['Date_Clean'].max()}"
)

# ============================================================
# 15. EXTRACT DURATION IN DAYS
# ============================================================

analysis_df["Duration_Days"] = (
    analysis_df["Duration"]
    .astype(str)
    .str.extract(r"(\d+)")
    [0]
)

analysis_df["Duration_Days"] = pd.to_numeric(
    analysis_df["Duration_Days"],
    errors="coerce"
)

# ============================================================
# 16. DERIVED MARKETING METRICS
#
# These are NEW columns.
# Original 22 columns remain unchanged.
# ============================================================

print("\n[13] CREATING DERIVED METRICS")
print("-" * 80)

# ------------------------------------------------------------
# CTR = Click Through Rate
# ------------------------------------------------------------

analysis_df["CTR"] = np.where(
    analysis_df["Impressions"] > 0,
    analysis_df["Clicks"] / analysis_df["Impressions"],
    np.nan
)

# ------------------------------------------------------------
# Estimated Conversions
#
# Conversion_Rate is stored as decimal.
# Example:
# 0.04 = 4%
# ------------------------------------------------------------

analysis_df["Estimated_Conversions"] = (
    analysis_df["Clicks"] *
    analysis_df["Conversion_Rate"]
)

# ------------------------------------------------------------
# Cost Per Click
# ------------------------------------------------------------

analysis_df["Calculated_CPC"] = np.where(
    analysis_df["Clicks"] > 0,
    analysis_df["Acquisition_Cost_Clean"] /
    analysis_df["Clicks"],
    np.nan
)

# ------------------------------------------------------------
# Cost Per Estimated Acquisition
# ------------------------------------------------------------

analysis_df["Calculated_CPA"] = np.where(
    analysis_df["Estimated_Conversions"] > 0,
    analysis_df["Acquisition_Cost_Clean"] /
    analysis_df["Estimated_Conversions"],
    np.nan
)

# ------------------------------------------------------------
# Date components
# ------------------------------------------------------------

analysis_df["Year"] = analysis_df["Date_Clean"].dt.year
analysis_df["Month"] = analysis_df["Date_Clean"].dt.month
analysis_df["Month_Name"] = analysis_df["Date_Clean"].dt.month_name()
analysis_df["Year_Month"] = (
    analysis_df["Date_Clean"]
    .dt.to_period("M")
    .astype(str)
)

print("Derived metrics created.")

# ============================================================
# 17. KEY OVERALL METRICS
# ============================================================

print("\n[14] OVERALL MARKETING METRICS")
print("-" * 80)

overall_metrics = {
    "Total Campaigns": len(analysis_df),
    "Total Impressions": analysis_df["Impressions"].sum(),
    "Total Clicks": analysis_df["Clicks"].sum(),
    "Overall CTR": (
        analysis_df["Clicks"].sum() /
        analysis_df["Impressions"].sum()
    ),
    "Total Acquisition Cost": (
        analysis_df["Acquisition_Cost_Clean"].sum()
    ),
    "Average ROI": analysis_df["ROI"].mean(),
    "Average Conversion Rate": analysis_df["Conversion_Rate"].mean(),
    "Average Engagement Score": analysis_df["Engagement_Score"].mean(),
    "Estimated Total Conversions": (
        analysis_df["Estimated_Conversions"].sum()
    ),
    "Average CPC": analysis_df["Calculated_CPC"].mean(),
    "Average CPA": analysis_df["Calculated_CPA"].mean()
}

for metric, value in overall_metrics.items():

    if isinstance(value, (float, np.floating)):
        print(f"{metric:<35}: {value:,.4f}")
    else:
        print(f"{metric:<35}: {value:,.2f}")

overall_metrics_df = pd.DataFrame(
    list(overall_metrics.items()),
    columns=["Metric", "Value"]
)

overall_metrics_df.to_csv(
    EDA_DIR / "09_overall_metrics.csv",
    index=False
)

# ============================================================
# 18. CAMPAIGN TYPE ANALYSIS
# ============================================================

print("\n[15] CAMPAIGN TYPE ANALYSIS")
print("-" * 80)

campaign_type_analysis = (
    analysis_df
    .groupby("Campaign_Type")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=("Impressions", "sum"),
        Total_Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        ),
        Average_CPC=("Calculated_CPC", "mean"),
        Average_CPA=("Calculated_CPA", "mean")
    )
    .sort_values("Average_ROI", ascending=False)
)

print(campaign_type_analysis.to_string())

campaign_type_analysis.to_csv(
    EDA_DIR / "10_campaign_type_analysis.csv"
)

# ============================================================
# 19. COMPANY ANALYSIS
# ============================================================

print("\n[16] COMPANY ANALYSIS")
print("-" * 80)

company_analysis = (
    analysis_df
    .groupby("Company")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=("Impressions", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(company_analysis.to_string())

company_analysis.to_csv(
    EDA_DIR / "11_company_analysis.csv"
)

# ============================================================
# 20. CHANNEL ANALYSIS
# ============================================================

print("\n[17] CHANNEL ANALYSIS")
print("-" * 80)

channel_analysis = (
    analysis_df
    .groupby("Channel_Used")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=("Impressions", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(channel_analysis.to_string())

channel_analysis.to_csv(
    EDA_DIR / "12_channel_analysis.csv"
)

# ============================================================
# 21. TARGET AUDIENCE ANALYSIS
# ============================================================

print("\n[18] TARGET AUDIENCE ANALYSIS")
print("-" * 80)

audience_analysis = (
    analysis_df
    .groupby("Target_Audience")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(audience_analysis.to_string())

audience_analysis.to_csv(
    EDA_DIR / "13_target_audience_analysis.csv"
)

# ============================================================
# 22. LOCATION ANALYSIS
# ============================================================

print("\n[19] LOCATION ANALYSIS")
print("-" * 80)

location_analysis = (
    analysis_df
    .groupby("Location")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(location_analysis.to_string())

location_analysis.to_csv(
    EDA_DIR / "14_location_analysis.csv"
)

# ============================================================
# 23. LANGUAGE ANALYSIS
# ============================================================

print("\n[20] LANGUAGE ANALYSIS")
print("-" * 80)

language_analysis = (
    analysis_df
    .groupby("Language")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(language_analysis.to_string())

language_analysis.to_csv(
    EDA_DIR / "15_language_analysis.csv"
)

# ============================================================
# 24. CUSTOMER SEGMENT ANALYSIS
# ============================================================

print("\n[21] CUSTOMER SEGMENT ANALYSIS")
print("-" * 80)

segment_analysis = (
    analysis_df
    .groupby("Customer_Segment")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .sort_values("Average_ROI", ascending=False)
)

print(segment_analysis.to_string())

segment_analysis.to_csv(
    EDA_DIR / "16_customer_segment_analysis.csv"
)

# ============================================================
# 25. DURATION ANALYSIS
# ============================================================

print("\n[22] DURATION ANALYSIS")
print("-" * 80)

duration_analysis = (
    analysis_df
    .groupby("Duration_Days")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        )
    )
    .sort_index()
)

print(duration_analysis.to_string())

duration_analysis.to_csv(
    EDA_DIR / "17_duration_analysis.csv"
)

# ============================================================
# 26. MONTHLY ANALYSIS
# ============================================================

print("\n[23] MONTHLY ANALYSIS")
print("-" * 80)

monthly_analysis = (
    analysis_df
    .groupby("Year_Month")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=("Impressions", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Acquisition_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

print(monthly_analysis.head(20).to_string(index=False))

monthly_analysis.to_csv(
    EDA_DIR / "18_monthly_analysis.csv",
    index=False
)

# ============================================================
# 27. CORRELATION ANALYSIS
# ============================================================

print("\n[24] CORRELATION ANALYSIS")
print("-" * 80)

correlation_columns = [
    "Duration_Days",
    "Conversion_Rate",
    "Acquisition_Cost_Clean",
    "ROI",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "CTR",
    "Estimated_Conversions",
    "Calculated_CPC",
    "Calculated_CPA"
]

correlation_matrix = (
    analysis_df[correlation_columns]
    .corr()
)

print(correlation_matrix.round(3).to_string())

correlation_matrix.to_csv(
    EDA_DIR / "19_correlation_matrix.csv"
)

# ============================================================
# 28. VISUALIZATION SETTINGS
# ============================================================

sns.set_theme(style="whitegrid")

# ============================================================
# 29. CHART 1
# Campaign Type vs ROI
# ============================================================

plt.figure(figsize=(11, 6))

sns.barplot(
    data=campaign_type_analysis.reset_index(),
    x="Campaign_Type",
    y="Average_ROI"
)

plt.title("Average ROI by Campaign Type")
plt.xlabel("Campaign Type")
plt.ylabel("Average ROI")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    EDA_DIR / "20_campaign_type_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 30. CHART 2
# Channel vs ROI
# ============================================================

plt.figure(figsize=(11, 6))

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
    EDA_DIR / "21_channel_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 31. CHART 3
# Customer Segment vs ROI
# ============================================================

plt.figure(figsize=(12, 7))

sns.barplot(
    data=segment_analysis.reset_index(),
    x="Average_ROI",
    y="Customer_Segment"
)

plt.title("Average ROI by Customer Segment")
plt.xlabel("Average ROI")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "22_segment_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 32. CHART 4
# Location vs ROI
# ============================================================

top_locations = (
    location_analysis
    .head(15)
    .reset_index()
)

plt.figure(figsize=(12, 8))

sns.barplot(
    data=top_locations,
    x="Average_ROI",
    y="Location"
)

plt.title("Top Locations by Average ROI")
plt.xlabel("Average ROI")
plt.ylabel("Location")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "23_location_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 33. CHART 5
# Conversion Rate Distribution
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=analysis_df,
    x="Conversion_Rate",
    bins=30,
    kde=True
)

plt.title("Conversion Rate Distribution")
plt.xlabel("Conversion Rate")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "24_conversion_rate_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 34. CHART 6
# ROI Distribution
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=analysis_df,
    x="ROI",
    bins=30,
    kde=True
)

plt.title("ROI Distribution")
plt.xlabel("ROI")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "25_roi_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 35. CHART 7
# Acquisition Cost vs ROI
# ============================================================

plot_data = analysis_df.sample(
    min(10000, len(analysis_df)),
    random_state=42
)

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=plot_data,
    x="Acquisition_Cost_Clean",
    y="ROI",
    alpha=0.4
)

plt.title("Acquisition Cost vs ROI")
plt.xlabel("Acquisition Cost ($)")
plt.ylabel("ROI")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "26_cost_vs_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 36. CHART 8
# Clicks vs Estimated Conversions
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=plot_data,
    x="Clicks",
    y="Estimated_Conversions",
    alpha=0.4
)

plt.title("Clicks vs Estimated Conversions")
plt.xlabel("Clicks")
plt.ylabel("Estimated Conversions")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "27_clicks_vs_conversions.png",
    dpi=300
)

plt.close()

# ============================================================
# 37. CHART 9
# Engagement Score Distribution
# ============================================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=analysis_df,
    x="Engagement_Score"
)

plt.title("Engagement Score Distribution")
plt.xlabel("Engagement Score")
plt.ylabel("Number of Campaigns")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "28_engagement_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 38. CHART 10
# Monthly ROI
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
    EDA_DIR / "29_monthly_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 39. CHART 11
# Monthly Conversions
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_analysis["Year_Month"],
    monthly_analysis["Estimated_Conversions"],
    marker="o"
)

plt.title("Monthly Estimated Conversions")
plt.xlabel("Month")
plt.ylabel("Estimated Conversions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    EDA_DIR / "30_monthly_conversions.png",
    dpi=300
)

plt.close()

# ============================================================
# 40. CHART 12
# Correlation Heatmap
# ============================================================

plt.figure(figsize=(13, 10))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Marketing Metrics Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "31_correlation_heatmap.png",
    dpi=300
)

plt.close()

# ============================================================
# 41. TOP COMPANIES
# ============================================================

top_companies = (
    company_analysis
    .head(15)
    .reset_index()
)

plt.figure(figsize=(12, 8))

sns.barplot(
    data=top_companies,
    x="Average_ROI",
    y="Company"
)

plt.title("Top Companies by Average ROI")
plt.xlabel("Average ROI")
plt.ylabel("Company")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "32_top_companies_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 42. TARGET AUDIENCE CHART
# ============================================================

top_audiences = (
    audience_analysis
    .head(15)
    .reset_index()
)

plt.figure(figsize=(12, 8))

sns.barplot(
    data=top_audiences,
    x="Average_ROI",
    y="Target_Audience"
)

plt.title("Top Target Audiences by Average ROI")
plt.xlabel("Average ROI")
plt.ylabel("Target Audience")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "33_target_audience_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 43. LANGUAGE CHART
# ============================================================

plt.figure(figsize=(11, 6))

sns.barplot(
    data=language_analysis.reset_index(),
    x="Language",
    y="Average_ROI"
)

plt.title("Average ROI by Language")
plt.xlabel("Language")
plt.ylabel("Average ROI")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    EDA_DIR / "34_language_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 44. DURATION VS ROI
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=duration_analysis.reset_index(),
    x="Duration_Days",
    y="Average_ROI"
)

plt.title("Average ROI by Campaign Duration")
plt.xlabel("Duration (Days)")
plt.ylabel("Average ROI")
plt.tight_layout()

plt.savefig(
    EDA_DIR / "35_duration_roi.png",
    dpi=300
)

plt.close()

# ============================================================
# 45. SAVE ANALYSIS DATA
# ============================================================

print("\n[25] SAVING EDA DATA")
print("-" * 80)

# Save analysis dataframe separately.
# Original 22 columns are preserved + derived columns.

analysis_df.to_csv(
    EDA_DIR / "eda_dataset_with_derived_metrics.csv",
    index=False
)

print("EDA dataset saved.")

# ============================================================
# 46. VERIFY ORIGINAL COLUMNS WERE PRESERVED
# ============================================================

print("\n[26] ORIGINAL COLUMN VERIFICATION")
print("-" * 80)

missing_original_columns = [
    column
    for column in original_columns
    if column not in analysis_df.columns
]

if len(missing_original_columns) == 0:
    print("All 22 original columns are preserved. ✅")
else:
    print("WARNING - Missing original columns:")
    for column in missing_original_columns:
        print(f"- {column}")

# ============================================================
# 47. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("EDA COMPLETED SUCCESSFULLY!")
print("=" * 80)

print(f"Original rows    : {len(df):,}")
print(f"Original columns : {len(original_columns)}")
print(f"EDA rows         : {len(analysis_df):,}")
print(f"EDA columns      : {len(analysis_df.columns)}")

print("\nOriginal 22 columns preserved: YES ✅")

print("\nEDA output folder:")
print(EDA_DIR)

print("\nGenerated files:")

for file in sorted(EDA_DIR.iterdir()):
    print(f" - {file.name}")

print("\n" + "=" * 80)
print("NEXT: BUSINESS INSIGHTS + DASHBOARD")
print("=" * 80)