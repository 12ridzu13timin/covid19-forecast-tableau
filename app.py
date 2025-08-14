import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# =========================
# Load Data Function
# =========================
@st.cache_data
def load_data(file_path="covidnewdata-2020-2022.xlsx"):
    df = pd.read_excel(file_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year

    if "total_cases" not in df.columns and "cases_new" in df.columns:
        df = df.sort_values("date")
        df["total_cases"] = df.groupby("state")["cases_new"].cumsum()

    return df

df = load_data()

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("MC - O31 ITIB4114-BUSINESS INTELLIGENCE-MAY 2025")
    st.markdown("""
    Welcome to our COVID-19 Dashboard.  
    This dashboard presents Malaysia’s COVID-19 cases (2020–2022) with interactive charts  
    and a 30-day forecast using Holt-Winters Exponential Smoothing.
    """)
    st.divider()
    st.header("Filters")

    if "year" in df.columns:
        years = st.multiselect(
            "Year(s)",
            options=sorted(df["year"].dropna().unique()),
            default=sorted(df["year"].dropna().unique())
        )
    else:
        years = []

    if "state" in df.columns:
        states = st.multiselect(
            "State(s)",
            options=sorted(df["state"].dropna().unique()),
            default=sorted(df["state"].dropna().unique())
        )
    else:
        states = []

# =========================
# Filter Data
# =========================
filtered_df = df.copy()
if years:
    filtered_df = filtered_df[filtered_df["year"].isin(years)]
if states:
    filtered_df = filtered_df[filtered_df["state"].isin(states)]

# =========================
# Total Cases Over Time
# =========================
st.container()
st.subheader("Total Cases Over Time")
if "total_cases" in filtered_df.columns:
    total_cases_by_date = (
        filtered_df.groupby("date")["total_cases"]
        .sum()
        .reset_index()
    )
    fig_total_cases = px.line(
        total_cases_by_date,
        x="date",
        y="total_cases",
        title="Total COVID-19 Cases Over Time",
        labels={"total_cases": "Total Cases", "date": "Date"}
    )
    st.plotly_chart(fig_total_cases, use_container_width=True)
else:
    st.warning("Column 'total_cases' not found in dataset.")

# =========================
# Daily New Cases
# =========================
st.container()
st.subheader("Daily New Cases")
if "cases_new" in filtered_df.columns:
    daily_cases_by_date = (
        filtered_df.groupby("date")["cases_new"]
        .sum()
        .reset_index()
    )
    fig_daily_cases = px.bar(
        daily_cases_by_date,
        x="date",
        y="cases_new",
        title="Daily New COVID-19 Cases",
        labels={"cases_new": "New Cases", "date": "Date"}
    )
    st.plotly_chart(fig_daily_cases, use_container_width=True)
else:
    st.warning("Column 'cases_new' not found in dataset.")

# =========================
# Forecasting (30 days)
# =========================
st.container()
st.subheader("30-Day Forecast")
if "total_cases" in filtered_df.columns:
    total_cases_by_date = (
        filtered_df.groupby("date")["total_cases"]
        .sum()
        .reset_index()
    )
    total_cases_by_date = total_cases_by_date.sort_values("date")

    try:
        model = ExponentialSmoothing(
            total_cases_by_date["total_cases"],
            trend="add",
            seasonal=None
        ).fit()
        forecast = model.forecast(30)
        forecast_dates = pd.date_range(
            start=total_cases_by_date["date"].iloc[-1] + pd.Timedelta(days=1),
            periods=30
        )
        forecast_df = pd.DataFrame({"date": forecast_dates, "forecasted_cases": forecast})

        fig_forecast = px.line(
            total_cases_by_date,
            x="date",
            y="total_cases",
            title="30-Day Forecast of Total COVID-19 Cases",
            labels={"total_cases": "Total Cases", "date": "Date"}
        )
        fig_forecast.add_scatter(
            x=forecast_df["date"],
            y=forecast_df["forecasted_cases"],
            mode="lines",
            name="Forecast"
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
    except Exception as e:
        st.error(f"Forecasting error: {e}")
else:
    st.warning("Column 'total_cases' not found in dataset.")

# =========================
# Cases by State
# =========================
st.container()
st.subheader("Cases by State")
if "state" in filtered_df.columns and "cases_new" in filtered_df.columns:
    cases_by_state = (
        filtered_df.groupby("state")["cases_new"]
        .sum()
        .reset_index()
        .sort_values("cases_new", ascending=False)
    )
    fig_state_cases = px.bar(
        cases_by_state,
        x="state",
        y="cases_new",
        title="Total Cases by State",
        labels={"cases_new": "New Cases", "state": "State"}
    )
    st.plotly_chart(fig_state_cases, use_container_width=True)
else:
    st.warning("Required columns 'state' or 'cases_new' not found in dataset.")
