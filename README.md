# Music Streaming App Subscription Prediction

## Project Overview

This project explores which user behaviors and characteristics are associated with conversion from a free trial to a paid Premium subscription in a music streaming app.

The analysis focuses on user demographics, account characteristics, onboarding behavior, and trial-period engagement metrics. The main goal is to identify useful proxy metrics for Premium conversion and translate them into business insights.

The project uses exploratory data analysis, statistical association testing, predictor overlap checks, multicollinearity analysis, and a composite trial engagement metric.

## Repository Structure

```text
music-app-proxy-metrics-analysis/
│
├── data/
│   └── music_streaming_app_source.scv
│
├── notebooks/
│   └── Music_Streaming_App_Subscription_Proxy_Research.ipynb
│
├── src/
│   ├── visual.py
│   └── styles.py
│
└── README.md
```

## Main Methods

The analysis includes:

- basic data quality checks

- exploratory data analysis

- conversion comparison by feature

- point-biserial correlation for numeric features

- Chi-square tests with Phi coefficient for binary features

- Chi-square test with Cramér’s V for categorical features

- Spearman correlation to check predictor overlap

- VIF to check multicollinearity

- Trial Engagement Index construction
