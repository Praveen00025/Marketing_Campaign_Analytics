 # ============================================================
# MARKETING CAMPAIGN ANALYTICS
# BUSINESS INSIGHTS
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
EDA_DIR = PROJECT_DIR / "eda_output"
OUTPUT_DIR = PROJECT_DIR / "business_output"

OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("MARKETING CAMPAIGN ANALYTICS - BUSINESS INSIGHTS")
print("=" * 80)

# ============================================================
# 2. LOAD EDA DATA
# ============================================================

EDA_FILE = EDA_DIR / "eda_dataset_with_derived_metrics.csv"

if not EDA_FILE.exists():
    print("ERROR: EDA dataset not found!")
    print(f"Expected file: {EDA_FILE}")
    exit()

df = pd.read_csv(EDA_FILE)

print(f"\nDataset loaded successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# 3. DATA PREPARATION
# ============================================================

print("\n[1] Preparing business analysis data...")
print("-" * 80)

# Convert numeric columns
numeric_columns = [
    "Conversion_Rate",
    "Acquisition_Cost_Clean",
    "ROI",
    "Clicks",
    "Impressions",
    "Engagement_Score",
    "CTR",
    "Estimated_Conversions",
    "Calculated_CPC",
    "Calculated_CPA",
    "Duration_Days"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# ============================================================
# 4. OVERALL BUSINESS KPIs
# ============================================================

print("\n[2] OVERALL BUSINESS KPIs")
print("=" * 80)

total_campaigns = len(df)

total_impressions = df["Impressions"].sum()

total_clicks = df["Clicks"].sum()

total_cost = df["Acquisition_Cost_Clean"].sum()

average_roi = df["ROI"].mean()

average_conversion_rate = df["Conversion_Rate"].mean()

average_engagement = df["Engagement_Score"].mean()

total_estimated_conversions = (
    df["Estimated_Conversions"].sum()
)

overall_ctr = (
    total_clicks / total_impressions
    if total_impressions > 0
    else np.nan
)

average_cpc = (
    total_cost / total_clicks
    if total_clicks > 0
    else np.nan
)

average_cpa = (
    total_cost / total_estimated_conversions
    if total_estimated_conversions > 0
    else np.nan
)

kpis = {
    "Total Campaigns": total_campaigns,
    "Total Impressions": total_impressions,
    "Total Clicks": total_clicks,
    "Total Acquisition Cost": total_cost,
    "Average ROI": average_roi,
    "Average Conversion Rate": average_conversion_rate,
    "Overall CTR": overall_ctr,
    "Average Engagement Score": average_engagement,
    "Estimated Total Conversions": total_estimated_conversions,
    "Average CPC": average_cpc,
    "Average CPA": average_cpa
}

for name, value in kpis.items():
    print(f"{name:<35}: {value:,.4f}")

kpi_df = pd.DataFrame(
    list(kpis.items()),
    columns=["KPI", "Value"]
)

kpi_df.to_csv(
    OUTPUT_DIR / "01_business_kpis.csv",
    index=False
)

# ============================================================
# 5. CAMPAIGN TYPE INSIGHTS
# ============================================================

print("\n[3] CAMPAIGN TYPE INSIGHTS")
print("=" * 80)

campaign_type = (
    df.groupby("Campaign_Type")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=(
            "Impressions",
            "sum"
        ),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

campaign_type["CTR"] = (
    campaign_type["Total_Clicks"] /
    campaign_type["Total_Impressions"]
)

campaign_type["CPC"] = (
    campaign_type["Total_Cost"] /
    campaign_type["Total_Clicks"]
)

campaign_type["CPA"] = (
    campaign_type["Total_Cost"] /
    campaign_type["Estimated_Conversions"]
)

campaign_type = campaign_type.sort_values(
    "Average_ROI",
    ascending=False
)

print(campaign_type.to_string(index=False))

campaign_type.to_csv(
    OUTPUT_DIR / "02_campaign_type_insights.csv",
    index=False
)

# ============================================================
# 6. CHANNEL INSIGHTS
# ============================================================

print("\n[4] MARKETING CHANNEL INSIGHTS")
print("=" * 80)

channel = (
    df.groupby("Channel_Used")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=(
            "Impressions",
            "sum"
        ),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

channel["CTR"] = (
    channel["Total_Clicks"] /
    channel["Total_Impressions"]
)

channel["CPC"] = (
    channel["Total_Cost"] /
    channel["Total_Clicks"]
)

channel["CPA"] = (
    channel["Total_Cost"] /
    channel["Estimated_Conversions"]
)

channel = channel.sort_values(
    "Average_ROI",
    ascending=False
)

print(channel.to_string(index=False))

channel.to_csv(
    OUTPUT_DIR / "03_channel_insights.csv",
    index=False
)

# ============================================================
# 7. COMPANY INSIGHTS
# ============================================================

print("\n[5] COMPANY INSIGHTS")
print("=" * 80)

company = (
    df.groupby("Company")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=(
            "Impressions",
            "sum"
        ),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

company["CTR"] = (
    company["Total_Clicks"] /
    company["Total_Impressions"]
)

company["CPC"] = (
    company["Total_Cost"] /
    company["Total_Clicks"]
)

company["CPA"] = (
    company["Total_Cost"] /
    company["Estimated_Conversions"]
)

company = company.sort_values(
    "Average_ROI",
    ascending=False
)

print(company.head(20).to_string(index=False))

company.to_csv(
    OUTPUT_DIR / "04_company_insights.csv",
    index=False
)

# ============================================================
# 8. TARGET AUDIENCE INSIGHTS
# ============================================================

print("\n[6] TARGET AUDIENCE INSIGHTS")
print("=" * 80)

audience = (
    df.groupby("Target_Audience")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

audience["CPC"] = (
    audience["Total_Cost"] /
    audience["Total_Clicks"]
)

audience["CPA"] = (
    audience["Total_Cost"] /
    audience["Estimated_Conversions"]
)

audience = audience.sort_values(
    "Average_ROI",
    ascending=False
)

print(audience.to_string(index=False))

audience.to_csv(
    OUTPUT_DIR / "05_target_audience_insights.csv",
    index=False
)

# ============================================================
# 9. CUSTOMER SEGMENT INSIGHTS
# ============================================================

print("\n[7] CUSTOMER SEGMENT INSIGHTS")
print("=" * 80)

segment = (
    df.groupby("Customer_Segment")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

segment["CPC"] = (
    segment["Total_Cost"] /
    segment["Total_Clicks"]
)

segment["CPA"] = (
    segment["Total_Cost"] /
    segment["Estimated_Conversions"]
)

segment = segment.sort_values(
    "Average_ROI",
    ascending=False
)

print(segment.to_string(index=False))

segment.to_csv(
    OUTPUT_DIR / "06_customer_segment_insights.csv",
    index=False
)

# ============================================================
# 10. LOCATION INSIGHTS
# ============================================================

print("\n[8] LOCATION INSIGHTS")
print("=" * 80)

location = (
    df.groupby("Location")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

location["CPC"] = (
    location["Total_Cost"] /
    location["Total_Clicks"]
)

location["CPA"] = (
    location["Total_Cost"] /
    location["Estimated_Conversions"]
)

location = location.sort_values(
    "Average_ROI",
    ascending=False
)

print(location.head(20).to_string(index=False))

location.to_csv(
    OUTPUT_DIR / "07_location_insights.csv",
    index=False
)

# ============================================================
# 11. LANGUAGE INSIGHTS
# ============================================================

print("\n[9] LANGUAGE INSIGHTS")
print("=" * 80)

language = (
    df.groupby("Language")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        )
    )
    .reset_index()
)

language = language.sort_values(
    "Average_ROI",
    ascending=False
)

print(language.to_string(index=False))

language.to_csv(
    OUTPUT_DIR / "08_language_insights.csv",
    index=False
)

# ============================================================
# 12. CAMPAIGN DURATION INSIGHTS
# ============================================================

print("\n[10] CAMPAIGN DURATION INSIGHTS")
print("=" * 80)

duration = (
    df.groupby("Duration_Days")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        )
    )
    .reset_index()
    .sort_values("Duration_Days")
)

print(duration.to_string(index=False))

duration.to_csv(
    OUTPUT_DIR / "09_duration_insights.csv",
    index=False
)

# ============================================================
# 13. MONTHLY PERFORMANCE
# ============================================================

print("\n[11] MONTHLY PERFORMANCE")
print("=" * 80)

monthly = (
    df.groupby("Year_Month")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Average_ROI=("ROI", "mean"),
        Average_Conversion_Rate=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Total_Clicks=("Clicks", "sum"),
        Total_Impressions=(
            "Impressions",
            "sum"
        ),
        Estimated_Conversions=(
            "Estimated_Conversions",
            "sum"
        ),
        Total_Cost=(
            "Acquisition_Cost_Clean",
            "sum"
        )
    )
    .reset_index()
)

monthly["CTR"] = (
    monthly["Total_Clicks"] /
    monthly["Total_Impressions"]
)

monthly = monthly.sort_values("Year_Month")

print(monthly.to_string(index=False))

monthly.to_csv(
    OUTPUT_DIR / "10_monthly_performance.csv",
    index=False
)

# ============================================================
# 14. CORRELATION INSIGHTS
# ============================================================

print("\n[12] CORRELATION ANALYSIS")
print("=" * 80)

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

correlation = df[
    correlation_columns
].corr()

print(correlation.round(3).to_string())

correlation.to_csv(
    OUTPUT_DIR / "11_correlation_analysis.csv"
)

# ============================================================
# 15. AUTOMATIC INSIGHT GENERATION
# ============================================================

print("\n[13] AUTOMATIC BUSINESS INSIGHTS")
print("=" * 80)

insights = []

# ------------------------------------------------------------
# Campaign Type
# ------------------------------------------------------------

best_campaign_roi = campaign_type.iloc[0]

insights.append(
    f"Campaign type with highest average ROI: "
    f"{best_campaign_roi['Campaign_Type']} "
    f"({best_campaign_roi['Average_ROI']:.2f})"
)

highest_conversion_campaign = (
    campaign_type
    .sort_values(
        "Average_Conversion_Rate",
        ascending=False
    )
    .iloc[0]
)

insights.append(
    f"Campaign type with highest average conversion rate: "
    f"{highest_conversion_campaign['Campaign_Type']} "
    f"({highest_conversion_campaign['Average_Conversion_Rate']:.2%})"
)

# ------------------------------------------------------------
# Channel
# ------------------------------------------------------------

best_channel_roi = channel.iloc[0]

insights.append(
    f"Channel with highest average ROI: "
    f"{best_channel_roi['Channel_Used']} "
    f"({best_channel_roi['Average_ROI']:.2f})"
)

highest_channel_conversion = (
    channel
    .sort_values(
        "Average_Conversion_Rate",
        ascending=False
    )
    .iloc[0]
)

insights.append(
    f"Channel with highest average conversion rate: "
    f"{highest_channel_conversion['Channel_Used']} "
    f"({highest_channel_conversion['Average_Conversion_Rate']:.2%})"
)

# ------------------------------------------------------------
# Company
# ------------------------------------------------------------

best_company = company.iloc[0]

insights.append(
    f"Company with highest average ROI in the dataset: "
    f"{best_company['Company']} "
    f"({best_company['Average_ROI']:.2f})"
)

# ------------------------------------------------------------
# Customer Segment
# ------------------------------------------------------------

best_segment = segment.iloc[0]

insights.append(
    f"Customer segment with highest average ROI: "
    f"{best_segment['Customer_Segment']} "
    f"({best_segment['Average_ROI']:.2f})"
)

# ------------------------------------------------------------
# Location
# ------------------------------------------------------------

best_location = location.iloc[0]

insights.append(
    f"Location with highest average ROI: "
    f"{best_location['Location']} "
    f"({best_location['Average_ROI']:.2f})"
)

# ------------------------------------------------------------
# Language
# ------------------------------------------------------------

best_language = language.iloc[0]

insights.append(
    f"Language category with highest average ROI: "
    f"{best_language['Language']} "
    f"({best_language['Average_ROI']:.2f})"
)

# ------------------------------------------------------------
# Duration
# ------------------------------------------------------------

best_duration = (
    duration
    .sort_values(
        "Average_ROI",
        ascending=False
    )
    .iloc[0]
)

insights.append(
    f"Campaign duration with highest average ROI: "
    f"{best_duration['Duration_Days']:.0f} days "
    f"({best_duration['Average_ROI']:.2f})"
)

# ------------------------------------------------------------
# Overall CTR
# ------------------------------------------------------------

insights.append(
    f"Overall click-through rate (CTR): "
    f"{overall_ctr:.2%}"
)

# ------------------------------------------------------------
# Overall ROI
# ------------------------------------------------------------

insights.append(
    f"Overall average ROI across campaigns: "
    f"{average_roi:.2f}"
)

# ============================================================
# 16. PRINT INSIGHTS
# ============================================================

for number, insight in enumerate(insights, 1):
    print(f"{number}. {insight}")

# ============================================================
# 17. SAVE INSIGHTS
# ============================================================

insight_df = pd.DataFrame({
    "Insight_Number": range(1, len(insights) + 1),
    "Business_Insight": insights
})

insight_df.to_csv(
    OUTPUT_DIR / "12_business_insights.csv",
    index=False
)

# Also save as TXT
with open(
    OUTPUT_DIR / "business_insights.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "MARKETING CAMPAIGN ANALYTICS - BUSINESS INSIGHTS\n"
    )

    file.write("=" * 80 + "\n\n")

    for number, insight in enumerate(insights, 1):
        file.write(
            f"{number}. {insight}\n"
        )

# ============================================================
# 18. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("BUSINESS INSIGHTS COMPLETED!")
print("=" * 80)

print(f"\nRows analyzed    : {len(df):,}")
print(f"Columns analyzed : {len(df.columns)}")

print("\nBusiness output folder:")
print(OUTPUT_DIR)

print("\nGenerated files:")

for file in sorted(OUTPUT_DIR.iterdir()):
    print(f" - {file.name}")

print("\n" + "=" * 80)
print("NEXT STEP: INTERACTIVE DASHBOARD")
print("=" * 80)