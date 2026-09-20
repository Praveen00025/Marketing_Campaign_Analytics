# Marketing Campaign Analytics

An end-to-end data analytics project analyzing 200,000 marketing campaigns to understand campaign performance, ROI, conversion rates, customer segments, marketing channels, locations, and business performance.

## Project Overview

This project performs complete marketing campaign analysis using Python and provides an interactive Streamlit dashboard.

## Dataset

- Rows: 200,000
- Original Columns: 22
- Original dataset: `45.csv`

The original dataset structure is preserved.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## Project Features

### Data Validation

- Row count validation
- Column count validation
- Missing-value analysis
- Duplicate detection
- Data-type validation
- Column structure verification

### Exploratory Data Analysis

The project analyzes:

- ROI
- Conversion Rate
- Acquisition Cost
- Clicks
- Impressions
- Engagement Score
- Campaign Duration
- Campaign Type
- Marketing Channel
- Company
- Location
- Language
- Customer Segment
- Target Audience
- Monthly Performance

### Business Insights

Business-level analysis includes:

- Campaign type performance
- Channel performance
- Company performance
- Customer segment performance
- Location performance
- Target audience performance
- Language performance
- Campaign duration analysis
- Monthly ROI
- Conversion performance
- Acquisition cost analysis

## Interactive Dashboard

The Streamlit dashboard provides interactive filters and visualizations for:

- Company
- Campaign Type
- Marketing Channel
- Customer Segment
- Location
- Language

### Dashboard KPIs

- Total Campaigns
- Total Impressions
- Total Clicks
- Average ROI
- Conversion Rate
- CTR
- Engagement Score
- Estimated Conversions
- Total Acquisition Cost
- Average CPC
- Average CPA

## Project Structure

```text
Marketing_Campaign_Analytics/
│
├── 45.csv
├── analysis.py
├── validation.py
├── eda.py
├── business_insights.py
├── dashboard.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── output/
├── eda_output/
└── buisness output/