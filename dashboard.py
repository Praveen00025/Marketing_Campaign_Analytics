# ============================================================
# MARKETING CAMPAIGN ANALYTICS DASHBOARD
# Interactive Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Marketing Campaign Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    PROJECT_DIR
    / "eda_output"
    / "eda_dataset_with_derived_metrics.csv"
)


# ============================================================
# 3. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 25px;
    }

    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.25);
        padding: 15px;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)

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

    if "Date_Clean" in df.columns:

        df["Date_Clean"] = pd.to_datetime(
            df["Date_Clean"],
            errors="coerce"
        )

    return df


# ============================================================
# 5. CHECK DATA
# ============================================================

if not DATA_FILE.exists():

    st.error(
        "EDA dataset not found. Please run eda.py first."
    )

    st.stop()


df = load_data()


# ============================================================
# 6. HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📊 Marketing Campaign Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "Interactive analysis of campaign performance, ROI, "
    "conversion, engagement and customer segments."
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# 7. SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the campaigns."
)


# Company
companies = sorted(
    df["Company"]
    .dropna()
    .unique()
    .tolist()
)

selected_companies = st.sidebar.multiselect(
    "Company",
    companies,
    default=companies
)


# Campaign Type
campaign_types = sorted(
    df["Campaign_Type"]
    .dropna()
    .unique()
    .tolist()
)

selected_campaign_types = st.sidebar.multiselect(
    "Campaign Type",
    campaign_types,
    default=campaign_types
)


# Channel
channels = sorted(
    df["Channel_Used"]
    .dropna()
    .unique()
    .tolist()
)

selected_channels = st.sidebar.multiselect(
    "Marketing Channel",
    channels,
    default=channels
)


# Customer Segment
segments = sorted(
    df["Customer_Segment"]
    .dropna()
    .unique()
    .tolist()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)


# Location
locations = sorted(
    df["Location"]
    .dropna()
    .unique()
    .tolist()
)

selected_locations = st.sidebar.multiselect(
    "Location",
    locations,
    default=locations
)


# Language
languages = sorted(
    df["Language"]
    .dropna()
    .unique()
    .tolist()
)

selected_languages = st.sidebar.multiselect(
    "Language",
    languages,
    default=languages
)


# ============================================================
# 8. APPLY FILTERS
# ============================================================

filtered_df = df[
    df["Company"].isin(selected_companies)
    &
    df["Campaign_Type"].isin(selected_campaign_types)
    &
    df["Channel_Used"].isin(selected_channels)
    &
    df["Customer_Segment"].isin(selected_segments)
    &
    df["Location"].isin(selected_locations)
    &
    df["Language"].isin(selected_languages)
].copy()


# ============================================================
# 9. EMPTY FILTER CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No campaigns match the selected filters."
    )

    st.stop()


# ============================================================
# 10. CALCULATE KPIs
# ============================================================

total_campaigns = len(filtered_df)

total_impressions = (
    filtered_df["Impressions"].sum()
)

total_clicks = (
    filtered_df["Clicks"].sum()
)

total_cost = (
    filtered_df["Acquisition_Cost_Clean"].sum()
)

average_roi = (
    filtered_df["ROI"].mean()
)

average_conversion = (
    filtered_df["Conversion_Rate"].mean()
)

average_engagement = (
    filtered_df["Engagement_Score"].mean()
)

estimated_conversions = (
    filtered_df["Estimated_Conversions"].sum()
)

overall_ctr = (
    total_clicks / total_impressions
    if total_impressions > 0
    else 0
)

average_cpc = (
    total_cost / total_clicks
    if total_clicks > 0
    else 0
)

average_cpa = (
    total_cost / estimated_conversions
    if estimated_conversions > 0
    else 0
)


# ============================================================
# 11. KPI CARDS
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Campaigns",
        f"{total_campaigns:,}"
    )

with col2:
    st.metric(
        "Average ROI",
        f"{average_roi:.2f}"
    )

with col3:
    st.metric(
        "Conversion Rate",
        f"{average_conversion:.2%}"
    )

with col4:
    st.metric(
        "Engagement Score",
        f"{average_engagement:.2f}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Impressions",
        f"{total_impressions:,.0f}"
    )

with col6:
    st.metric(
        "Clicks",
        f"{total_clicks:,.0f}"
    )

with col7:
    st.metric(
        "CTR",
        f"{overall_ctr:.2%}"
    )

with col8:
    st.metric(
        "Estimated Conversions",
        f"{estimated_conversions:,.0f}"
    )


# ============================================================
# 12. COST METRICS
# ============================================================

st.subheader("💰 Cost Metrics")

cost1, cost2, cost3 = st.columns(3)

with cost1:
    st.metric(
        "Total Acquisition Cost",
        f"${total_cost:,.2f}"
    )

with cost2:
    st.metric(
        "Average CPC",
        f"${average_cpc:,.2f}"
    )

with cost3:
    st.metric(
        "Average CPA",
        f"${average_cpa:,.2f}"
    )


# ============================================================
# 13. CAMPAIGN TYPE ANALYSIS
# ============================================================

st.subheader("📣 Campaign Type Performance")

campaign_type_df = (
    filtered_df
    .groupby("Campaign_Type")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        campaign_type_df,
        x="Campaign_Type",
        y="Average_ROI",
        title="Average ROI by Campaign Type",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Campaign Type",
        yaxis_title="Average ROI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        campaign_type_df,
        x="Campaign_Type",
        y="Average_Conversion",
        title="Conversion Rate by Campaign Type",
        text_auto=".2%"
    )

    fig.update_layout(
        xaxis_title="Campaign Type",
        yaxis_title="Conversion Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 14. CHANNEL ANALYSIS
# ============================================================

st.subheader("📱 Marketing Channel Performance")

channel_df = (
    filtered_df
    .groupby("Channel_Used")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        channel_df,
        x="Channel_Used",
        y="Average_ROI",
        title="ROI by Marketing Channel",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Channel",
        yaxis_title="Average ROI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        channel_df,
        x="Channel_Used",
        y="Average_Engagement",
        title="Engagement by Marketing Channel",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Channel",
        yaxis_title="Engagement Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 15. CUSTOMER SEGMENT
# ============================================================

st.subheader("👥 Customer Segment Analysis")

segment_df = (
    filtered_df
    .groupby("Customer_Segment")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
)


fig = px.bar(
    segment_df,
    x="Customer_Segment",
    y="Average_ROI",
    color="Average_Engagement",
    title="Customer Segment Performance",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 16. LOCATION ANALYSIS
# ============================================================

st.subheader("🌍 Location Performance")

location_df = (
    filtered_df
    .groupby("Location")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
    .sort_values(
        "Average_ROI",
        ascending=False
    )
)


fig = px.bar(
    location_df.head(15),
    x="Average_ROI",
    y="Location",
    orientation="h",
    title="Top Locations by Average ROI",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 17. COMPANY ANALYSIS
# ============================================================

st.subheader("🏢 Company Performance")

company_df = (
    filtered_df
    .groupby("Company")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
    .sort_values(
        "Average_ROI",
        ascending=False
    )
)


fig = px.bar(
    company_df.head(15),
    x="Average_ROI",
    y="Company",
    orientation="h",
    title="Top Companies by Average ROI",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 18. TARGET AUDIENCE
# ============================================================

st.subheader("🎯 Target Audience Analysis")

audience_df = (
    filtered_df
    .groupby("Target_Audience")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=("Conversion_Rate", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
    .sort_values(
        "Average_ROI",
        ascending=False
    )
)


fig = px.bar(
    audience_df.head(15),
    x="Average_ROI",
    y="Target_Audience",
    orientation="h",
    title="Target Audience by Average ROI",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 19. ROI VS ACQUISITION COST
# ============================================================

st.subheader("💵 Acquisition Cost vs ROI")

scatter_data = filtered_df.sample(
    min(10000, len(filtered_df)),
    random_state=42
)


fig = px.scatter(
    scatter_data,
    x="Acquisition_Cost_Clean",
    y="ROI",
    color="Campaign_Type",
    hover_data=[
        "Company",
        "Channel_Used",
        "Location",
        "Customer_Segment"
    ],
    title="Acquisition Cost vs ROI",
    opacity=0.65
)

fig.update_layout(
    xaxis_title="Acquisition Cost ($)",
    yaxis_title="ROI"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 20. CLICKS VS CONVERSIONS
# ============================================================

st.subheader("🖱️ Clicks vs Estimated Conversions")

fig = px.scatter(
    scatter_data,
    x="Clicks",
    y="Estimated_Conversions",
    color="Channel_Used",
    hover_data=[
        "Company",
        "Campaign_Type",
        "Location"
    ],
    title="Clicks vs Estimated Conversions",
    opacity=0.65
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 21. MONTHLY PERFORMANCE
# ============================================================

st.subheader("📅 Monthly Performance")

if "Year_Month" in filtered_df.columns:

    monthly_df = (
        filtered_df
        .groupby("Year_Month")
        .agg(
            Average_ROI=("ROI", "mean"),
            Average_Conversion=(
                "Conversion_Rate",
                "mean"
            ),
            Estimated_Conversions=(
                "Estimated_Conversions",
                "sum"
            ),
            Campaigns=(
                "Campaign_ID",
                "count"
            )
        )
        .reset_index()
        .sort_values("Year_Month")
    )


    fig = px.line(
        monthly_df,
        x="Year_Month",
        y="Average_ROI",
        markers=True,
        title="Monthly Average ROI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    fig = px.line(
        monthly_df,
        x="Year_Month",
        y="Estimated_Conversions",
        markers=True,
        title="Monthly Estimated Conversions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 22. LANGUAGE ANALYSIS
# ============================================================

st.subheader("🌐 Language Performance")

language_df = (
    filtered_df
    .groupby("Language")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=(
            "Conversion_Rate",
            "mean"
        ),
        Average_Engagement=(
            "Engagement_Score",
            "mean"
        ),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
)


fig = px.bar(
    language_df,
    x="Language",
    y="Average_ROI",
    title="Average ROI by Language",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 23. CAMPAIGN DURATION
# ============================================================

st.subheader("⏱️ Campaign Duration Analysis")

duration_df = (
    filtered_df
    .groupby("Duration_Days")
    .agg(
        Average_ROI=("ROI", "mean"),
        Average_Conversion=(
            "Conversion_Rate",
            "mean"
        ),
        Campaigns=("Campaign_ID", "count")
    )
    .reset_index()
    .sort_values("Duration_Days")
)


fig = px.bar(
    duration_df,
    x="Duration_Days",
    y="Average_ROI",
    title="Average ROI by Campaign Duration",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 24. DATA TABLE
# ============================================================

st.subheader("📋 Campaign Data")

display_columns = [
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
    "Date"
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    height=400
)


# ============================================================
# 25. DOWNLOAD FILTERED DATA
# ============================================================

st.subheader("⬇️ Export Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Campaign Data",
    data=csv_data,
    file_name="filtered_marketing_campaign_data.csv",
    mime="text/csv"
)


# ============================================================
# 26. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Marketing Campaign Analytics | "
    "Python • Pandas • Plotly • Streamlit"
)