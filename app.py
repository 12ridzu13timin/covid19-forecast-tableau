import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# --------------------
# Load Data Function
# --------------------
@st.cache_data
def load_data(file_path="covidnewdata-2020-2022.xlsx"):
    df = pd.read_excel(file_path)

    # Clean column names to avoid KeyError
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Ensure date column is datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

# --------------------
# Forecast Function
# --------------------
def forecast_cases(data, periods=30):
    model = ExponentialSmoothing(
        data["total_cases"], 
        trend="add", 
        seasonal=None
    )
    fit = model.fit()
    forecast = fit.forecast(periods)
    return forecast

# --------------------
# Streamlit UI
# --------------------
st.set_page_config(page_title="COVID-19 Forecast Dashboard", layout="wide")
st.title("📊 COVID-19 Forecast Dashboard")

# Load dataset
df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
states = st.sidebar.multiselect(
    "Select State(s):", 
    options=df["state"].unique(), 
    default=df["state"].unique()
)

years = st.sidebar.multiselect(
    "Select Year(s):",
    options=df["date"].dt.year.unique(),
    default=df["date"].dt.year.unique()
)

filtered_df = df[
    df["state"].isin(states) & 
    df["date"].dt.year.isin(years)
]

# --------------------
# Section 1: Data Overview
# --------------------
with st.container():
    st.subheader("📋 Data Overview")
    st.dataframe(filtered_df)

# --------------------
# Section 2: Cases Over Time
# --------------------
with st.container():
    st.subheader("📈 Total Cases Over Time")
    if "total_cases" in filtered_df.columns:
        fig_cases = px.line(
            filtered_df.groupby("date")["total_cases"].sum().reset_index(),
            x="date", y="total_cases", title="Total COVID-19 Cases Over Time"
        )
        st.plotly_chart(fig_cases, use_container_width=True)
    else:
        st.error("Column 'total_cases' not found in dataset.")

# --------------------
# Section 3: Forecast
# --------------------
with st.container():
    st.subheader("🔮 30-Day Forecast")
    if "total_cases" in filtered_df.columns:
        grouped_data = filtered_df.groupby("date")["total_cases"].sum().reset_index()
        forecast_data = forecast_cases(grouped_data, periods=30)

        forecast_df = pd.DataFrame({
            "date": pd.date_range(start=grouped_data["date"].max() + pd.Timedelta(days=1), periods=30),
            "forecast_cases": forecast_data
        })

        fig_forecast = px.line(forecast_df, x="date", y="forecast_cases", title="30-Day Forecast of Cases")
        st.plotly_chart(fig_forecast, use_container_width=True)
    else:
        st.error("Column 'total_cases' not found in dataset.")

# --------------------
# Section 4: Raw Data Download
# --------------------
with st.container():
    st.subheader("⬇️ Download Filtered Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_covid_data.csv", "text/csv")
