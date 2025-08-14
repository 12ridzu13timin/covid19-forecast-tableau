import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# =========================
# Helpers
# =========================
def std_cols(df: pd.DataFrame) -> pd.DataFrame:
    # normalize column names
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(" ", "_").str.replace("-", "_")
    )

    def pick(cands):
        for c in cands:
            if c in df.columns:
                return c
        return None

    # guess important columns
    date_col   = pick(["date", "tarikh"])
    state_col  = pick(["state", "negeri", "region"])
    cases_col  = pick(["cases_new", "new_cases", "cases", "kes_baharu"])
    deaths_col = pick(["deaths_new", "new_deaths", "deaths", "kematian_baharu"])

    # rename to canonical if found
    rename_map = {}
    if date_col and date_col != "date": rename_map[date_col] = "date"
    if state_col and state_col != "state": rename_map[state_col] = "state"
    if cases_col and cases_col != "cases_new": rename_map[cases_col] = "cases_new"
    if deaths_col and deaths_col != "deaths_new": rename_map[deaths_col] = "deaths_new"
    if rename_map:
        df = df.rename(columns=rename_map)

    # parse date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["year"] = df["date"].dt.year

    # numeric safety
    for col in ["cases_new", "deaths_new"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

def daily_series(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Return daily totals across selected states, sorted by date."""
    s = (df.groupby("date")[value_col].sum()
         .reset_index().sort_values("date"))
    return s

def holt_winters_forecast(y: pd.Series, periods: int = 30):
    """Simple additive-trend ETS for daily values."""
    model = ExponentialSmoothing(y, trend="add", seasonal=None)
    fit = model.fit()
    fcst = fit.forecast(periods)
    return fcst

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="MC-O31 Group 5 | COVID-19 Dashboard (2020–2022)",
    layout="wide"
)
st.title("MC-O31 Group 5 COVID-19 Dashboard — Forecast & Analysis (2020–2022)")

# =========================
# Load Data
# =========================
@st.cache_data
def load_data(path: str = "covidnewdata-2020-2022.xlsx"):
    df = pd.read_excel(path)
    return std_cols(df)

# If you prefer upload on Cloud, uncomment the uploader:
# up = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
# df = load_data(up) if up is not None else load_data()
df = load_data()  # uses your local/Repo file

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("MC - O31 ITIB4114-BUSINESS INTELLIGENCE-MAY 2025")
   st.markdown("""
**Welcome to our COVID-19 Dashboard.**  
This dashboard presents **Malaysia’s COVID-19 cases (2020–2022)** with interactive charts and a 30-day forecast using Holt-Winters Exponential Smoothing.  
""")
    st.divider()
    st.header(" Filters")

    if "year" in df.columns:
        years = st.multiselect(
            "Year(s)", options=sorted(df["year"].dropna().unique()),
            default=sorted(df["year"].dropna().unique())
        )
    else:
        years = []

    if "state" in df.columns:
        states = st.multiselect(
            "State(s)", options=sorted(df["state"].dropna().unique()),
            default=sorted(df["state"].dropna().unique())
        )
    else:
        states = []

# Apply filters safely
flt = df.copy()
if years:
    flt = flt[flt["year"].isin(years)]
if states:
    flt = flt[flt["state"].isin(states)]

# =========================
# KPIs
# =========================
st.subheader(" summary ")
if flt.empty or "cases_new" not in flt.columns:
    st.warning("No data after filtering, or `cases_new` column missing.")
else:
    k1, k2, k3 = st.columns(3)
    total_cases = int(flt["cases_new"].sum())
    total_deaths = int(flt["deaths_new"].sum()) if "deaths_new" in flt.columns else 0
    avg_daily = round(flt.groupby("date")["cases_new"].sum().mean(), 2)

    k1.metric("Total New Cases (filtered)", f"{total_cases:,}")
    k2.metric("Total New Deaths (filtered)", f"{total_deaths:,}")
    k3.metric("Avg Daily New Cases", f"{avg_daily:,}")

# =========================
# Charts
# =========================
if not flt.empty and "cases_new" in flt.columns:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(" Daily New Cases by State")
        st.plotly_chart(
            px.line(flt.sort_values("date"), x="date", y="cases_new", color="state",
                    labels={"cases_new":"New Cases","date":"Date","state":"State"}),
            use_container_width=True
        )
    with c2:
        st.subheader(" Daily New Deaths by State")
        if "deaths_new" in flt.columns:
            st.plotly_chart(
                px.line(flt.sort_values("date"), x="date", y="deaths_new", color="state",
                        labels={"deaths_new":"New Deaths","date":"Date","state":"State"}),
                use_container_width=True
            )
        else:
            st.info("No `deaths_new` column in this dataset.")

    st.subheader("Totals by State ")
    if "state" in flt.columns:
        totals = flt.groupby("state", as_index=False)["cases_new"].sum()
        st.plotly_chart(
            px.bar(totals.sort_values("cases_new", ascending=False),
                   x="state", y="cases_new",
                   labels={"state":"State","cases_new":"Total New Cases"}),
            use_container_width=True
        )

    # ---- Total Cases Over Time (CUMULATIVE from daily) ----
    st.subheader(" Total sum  Cases Over Time ")
    daily = daily_series(flt, "cases_new")
    daily["total_cases_cum"] = daily["cases_new"].cumsum()
    st.plotly_chart(
        px.line(daily, x="date", y="total_cases_cum",
                labels={"date":"Date","total_cases_cum":"Cumulative Cases"},
                title=None),
        use_container_width=True
    )

# =========================
# Forecasts
# =========================
st.header(" Forecasts")

if not flt.empty and "cases_new" in flt.columns:
    horizon = st.slider("Forecast horizon (days)", 14, 90, 30, step=7)

    # ---- Forecast DAILY NEW CASES ----
    st.subheader("Forecast: Daily New Cases")
    daily = daily_series(flt, "cases_new")
    if len(daily) >= 10 and daily["cases_new"].sum() > 0:
        fcst_daily = holt_winters_forecast(daily["cases_new"], periods=horizon)
        fcst_df = pd.DataFrame({
            "date": pd.date_range(daily["date"].iloc[-1] + pd.Timedelta(days=1), periods=horizon),
            "forecast_daily_cases": fcst_daily.values
        })
        fig_d = px.line(daily, x="date", y="cases_new", labels={"cases_new":"Daily New Cases"})
        fig_d.add_scatter(x=fcst_df["date"], y=fcst_df["forecast_daily_cases"],
                          mode="lines", name="Forecast")
        fig_d.update_layout(title="Daily New Cases: Actual + Forecast")
        st.plotly_chart(fig_d, use_container_width=True)
    else:
        st.info("Not enough history to forecast daily cases.")

    # ---- Forecast CUMULATIVE TOTAL CASES ----
    st.subheader("Forecast: Total Cases (Cumulative)")
    # Build cumulative actuals
    daily["cum_cases"] = daily["cases_new"].cumsum()
    # Forecast future daily, then cumulate on top of last actual
    if len(daily) >= 10 and daily["cases_new"].sum() > 0:
        fcst_daily2 = holt_winters_forecast(daily["cases_new"], periods=horizon)
        base = daily["cum_cases"].iloc[-1]
        cum_forecast_vals = base + pd.Series(fcst_daily2).cumsum().values
        fcst_cum_df = pd.DataFrame({
            "date": pd.date_range(daily["date"].iloc[-1] + pd.Timedelta(days=1), periods=horizon),
            "forecast_total_cases": cum_forecast_vals
        })
        fig_c = px.line(daily, x="date", y="cum_cases",
                        labels={"cum_cases":"Cumulative Cases"})
        fig_c.add_scatter(x=fcst_cum_df["date"], y=fcst_cum_df["forecast_total_cases"],
                          mode="lines", name="Forecast")
        fig_c.update_layout(title="Total Cases (Cumulative): Actual + Forecast")
        st.plotly_chart(fig_c, use_container_width=True)
    else:
        st.info("Not enough history to forecast cumulative totals.")
else:
    st.info("Load data and set filters to see forecasts.")

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Built with Streamlit • Data from Excel • Forecasts via Holt–Winters (statsmodels)")
