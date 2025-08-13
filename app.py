import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# --------------------
# Load Data Function
# --------------------
@st.cache_data
def load_data(file_path="covid_data.xlsx"):
    df = pd.read_excel(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df

# --------------------
# Forecast Function
# --------------------
def forecast_cases(df, periods=30):
    df = df.groupby("date")["total_cases"].sum().reset_index()
    df = df.sort_values("date")
    model = ExponentialSmoothing(df["total_cases"], trend="add", seasonal=None)
    fit = model.fit()
    forecast_values = fit.forecast(periods)
    forecast_dates = pd.date_range(start=df["date"].iloc[-1] + pd.Timedelta(days=1), periods=periods)
    forecast_df = pd.DataFrame({"date": forecast_dates, "forecast_total_cases": forecast_values})
    return forecast_df

# --------------------
# Streamlit Layout
# --------------------
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("📊 COVID-19 Dashboard with Forecasting")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
years = st.sidebar.multiselect(
    "Select Year(s):",
    options=df["date"].dt.year.unique(),
    default=df["date"].dt.year.unique()
)
regions = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["region"].unique(),
    default=df["region"].unique()
)

# Filtered data
filtered_df = df[df["date"].dt.year.isin(years) & df["region"].isin(regions)]

# --------------------
# General Information Box
# --------------------
with st.container():
    st.subheader("ℹ General COVID-19 Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", f"{filtered_df['total_cases'].sum():,}")
    col2.metric("Total Deaths", f"{filtered_df['total_deaths'].sum():,}")
    col3.metric("Total Recovered", f"{filtered_df['total_recovered'].sum():,}")

# --------------------
# Cases Over Time
# --------------------
with st.container():
    st.subheader("📈 Total Cases Over Time")
    fig_cases = px.line(
        filtered_df.groupby("date")["total_cases"].sum().reset_index(),
        x="date",
        y="total_cases",
        title="Total COVID-19 Cases Over Time"
    )
    st.plotly_chart(fig_cases, use_container_width=True)

# --------------------
# Forecast Section
# --------------------
with st.container():
    st.subheader("🔮 Forecasted Total Cases")
    forecast_df = forecast_cases(filtered_df)
    fig_forecast = px.line(forecast_df, x="date", y="forecast_total_cases", title="Forecasted Total Cases (Next 30 Days)")
    st.plotly_chart(fig_forecast, use_container_width=True)

# --------------------
# Cases by Region
# --------------------
with st.container():
    st.subheader("🌍 Cases by Region")
    fig_region = px.bar(
        filtered_df.groupby("region")["total_cases"].sum().reset_index(),
        x="region",
        y="total_cases",
        title="Total Cases by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)
