import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Climate Impact | Climate Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(content)


# ============================================================
# SAME UI / CSS AS OVERVIEW
# ============================================================

html("""
<style>

.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(0,190,220,0.16), transparent 30%),
        radial-gradient(circle at 100% 0%, rgba(100,70,200,0.16), transparent 30%),
        linear-gradient(135deg, #06111f, #0a1627 50%, #0d1423);
    color: #eef6ff;
}

#MainMenu, footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    z-index: 999999 !important;
}

[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
    visibility: visible !important;
    opacity: 1 !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    color: #dce8f5 !important;
}

[data-testid="stSidebarCollapsedControl"] button svg {
    display: none !important;
}

[data-testid="stSidebarCollapsedControl"] button::after {
    content: "☰";
    display: block !important;
    font-size: 23px !important;
    line-height: 1 !important;
    font-weight: 700 !important;
    color: #eaf4ff !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06111f, #07101c);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #dce8f5;
}

/* Hero */
.hero {
    position: relative;
    padding: 40px;
    border-radius: 26px;
    background: linear-gradient(
        135deg,
        rgba(20,105,130,0.45),
        rgba(55,48,120,0.40)
    );
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 25px 70px rgba(0,0,0,0.35);
    overflow: hidden;
    margin-bottom: 30px;
}

.hero-glow {
    position: absolute;
    width: 280px;
    height: 280px;
    right: -100px;
    top: -140px;
    border-radius: 50%;
    background: rgba(50,200,220,0.16);
    filter: blur(10px);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.live-badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 999px;
    background: rgba(50,220,170,0.10);
    border: 1px solid rgba(50,220,170,0.30);
    color: #63e6b8;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.1;
    color: #f6faff;
    margin-bottom: 14px;
}

.hero-subtitle {
    max-width: 920px;
    color: #a9bbce;
    font-size: 16px;
    line-height: 1.7;
}

/* KPI */
.kpi-card {
    min-height: 145px;
    padding: 22px;
    border-radius: 19px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.075),
        rgba(255,255,255,0.025)
    );
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 15px 35px rgba(0,0,0,0.20);
    backdrop-filter: blur(15px);
}

.kpi-icon {
    font-size: 23px;
    margin-bottom: 9px;
}

.kpi-label {
    color: #8195aa;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
}

.kpi-value {
    color: #f5f9ff;
    font-size: 27px;
    font-weight: 780;
}

/* Impact cards */
.impact-card {
    min-height: 165px;
    padding: 23px;
    border-radius: 19px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.065),
        rgba(255,255,255,0.025)
    );
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 15px 35px rgba(0,0,0,0.18);
}

.impact-label {
    color: #8195aa;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.impact-status {
    color: #f4f9ff;
    font-size: 24px;
    font-weight: 780;
    margin-bottom: 9px;
}

.impact-detail {
    color: #8297aa;
    font-size: 13px;
    line-height: 1.55;
}

/* Insight cards */
.insight-card {
    min-height: 125px;
    padding: 21px;
    border-radius: 18px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 30px rgba(0,0,0,0.16);
}

.insight-label {
    color: #7890a5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 9px;
}

.insight-value {
    color: #f3f8fd;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 6px;
}

.insight-detail {
    color: #8297aa;
    font-size: 13px;
    line-height: 1.5;
}

/* Controls */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 11px;
}

div[data-testid="stDateInput"] input {
    background: transparent !important;
    color: #eef6ff !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
}

div[data-testid="stDateInput"] button {
    background: transparent !important;
    border: 0 !important;
    color: #c9d9e8 !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(135deg, #11677c, #315d98);
    color: white;
    font-weight: 700;
}

/* Footer */
.footer {
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid rgba(255,255,255,0.07);
    text-align: center;
    color: #657b90;
    font-size: 12px;
    line-height: 1.8;
}

</style>
""")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/climate_history_cleaned.csv")

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    df = df.dropna(subset=["time"])
    df = df.sort_values("time").reset_index(drop=True)

    return df


try:
    climate_df = load_data()
except FileNotFoundError:
    st.error("❌ climate_history_cleaned.csv was not found.")
    st.info(
        "Make sure the file is inside: "
        "data/climate_history_cleaned.csv"
    )
    st.stop()


if climate_df.empty:
    st.error("The climate dataset is empty.")
    st.stop()


# ============================================================
# CREATE PROJECT INDICATORS IF MISSING
# ============================================================

def heat_indicator(temp):
    if pd.isna(temp):
        return "Unknown"
    elif temp < 25:
        return "Low"
    elif temp < 30:
        return "Moderate"
    elif temp < 35:
        return "High"
    else:
        return "Very High"


def rainfall_indicator(rain):
    if pd.isna(rain):
        return "Unknown"
    elif rain == 0:
        return "No Rain"
    elif rain < 2.5:
        return "Light"
    elif rain < 7.6:
        return "Moderate"
    elif rain < 15:
        return "Heavy"
    else:
        return "Very Heavy"


def air_pollution_indicator(aqi):
    if pd.isna(aqi):
        return "Unknown"
    elif aqi <= 20:
        return "Good"
    elif aqi <= 40:
        return "Fair"
    elif aqi <= 60:
        return "Moderate"
    elif aqi <= 80:
        return "Poor"
    elif aqi <= 100:
        return "Very Poor"
    else:
        return "Extremely Poor"


def environmental_status(row):
    if row["air_pollution_indicator"] in [
        "Very Poor",
        "Extremely Poor"
    ]:
        return "High Environmental Impact"

    elif row["heat_indicator"] in [
        "High",
        "Very High"
    ]:
        return "High Environmental Impact"

    elif row["rainfall_indicator"] in [
        "Heavy",
        "Very Heavy"
    ]:
        return "High Environmental Impact"

    elif (
        row["air_pollution_indicator"] == "Moderate"
        or row["heat_indicator"] == "Moderate"
        or row["rainfall_indicator"] == "Moderate"
    ):
        return "Moderate Environmental Impact"

    else:
        return "Low Environmental Impact"


if "heat_indicator" not in climate_df.columns:
    climate_df["heat_indicator"] = climate_df[
        "temperature_2m"
    ].apply(heat_indicator)

if "rainfall_indicator" not in climate_df.columns:
    climate_df["rainfall_indicator"] = climate_df[
        "precipitation"
    ].apply(rainfall_indicator)

if "air_pollution_indicator" not in climate_df.columns:
    climate_df["air_pollution_indicator"] = climate_df[
        "european_aqi"
    ].apply(air_pollution_indicator)

if "environmental_status" not in climate_df.columns:
    climate_df["environmental_status"] = climate_df.apply(
        environmental_status,
        axis=1
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div style="
        color:#f4f8ff;
        font-size:24px;
        font-weight:800;
    ">
        🌍 Climate Intelligence
    </div>

    <div style="
        color:#738aa0;
        font-size:12px;
        margin-top:5px;
        margin-bottom:25px;
    ">
        Environmental Monitoring Platform
    </div>
    """)

    st.markdown("### 🌍 Climate Impact")

    st.caption(
        "Understand combined heat, rainfall, and air-pollution indicators."
    )

    st.markdown("---")

    min_date = climate_df["time"].min().date()
    max_date = climate_df["time"].max().date()

    st.markdown("### 📅 Analysis Period")

    date_columns = st.columns(2)

    with date_columns[0]:
        start_date = st.date_input(
            "From",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="impact_start_date"
        )

    with date_columns[1]:
        end_date = st.date_input(
            "To",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="impact_end_date"
        )

    st.markdown("### 📊 Impact View")

    impact_view = st.selectbox(
        "View",
        [
            "Environmental Status",
            "Heat Indicator",
            "Rainfall Indicator",
            "Air Pollution Indicator"
        ],
        label_visibility="collapsed"
    )

    st.markdown("### ⚡ Quick Period")

    quick_period = st.radio(
        "Period",
        [
            "Custom",
            "Last 7 Days",
            "Last 14 Days",
            "Last 30 Days"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    html("""
    <div style="
        padding:15px;
        border-radius:14px;
        background:rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.07);
        color:#8196aa;
        font-size:12px;
        line-height:1.9;
    ">
        <b>IMPACT INDICATORS</b><br>
        🌡️ Heat<br>
        🌧️ Rainfall<br>
        🌫️ Air Pollution<br>
        🌍 Environmental Status
    </div>
    """)


# ============================================================
# FILTER DATA
# ============================================================

if quick_period != "Custom":

    days_map = {
        "Last 7 Days": 7,
        "Last 14 Days": 14,
        "Last 30 Days": 30
    }

    days = days_map[quick_period]

    end_timestamp = climate_df["time"].max()

    start_timestamp = (
        end_timestamp -
        pd.Timedelta(days=days)
    )

    filtered_df = climate_df[
        (climate_df["time"] >= start_timestamp) &
        (climate_df["time"] <= end_timestamp)
    ].copy()

else:

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    start_timestamp = pd.Timestamp(start_date)

    end_timestamp = (
        pd.Timestamp(end_date) +
        pd.Timedelta(days=1)
    )

    filtered_df = climate_df[
        (climate_df["time"] >= start_timestamp) &
        (climate_df["time"] < end_timestamp)
    ].copy()


if filtered_df.empty:
    st.warning("No climate-impact data is available for this period.")
    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================

latest = filtered_df.iloc[-1]

avg_temp = filtered_df["temperature_2m"].mean()
max_temp = filtered_df["temperature_2m"].max()

avg_aqi = filtered_df["european_aqi"].mean()
max_aqi = filtered_df["european_aqi"].max()

total_rain = filtered_df["precipitation"].sum()

high_impact_count = (
    filtered_df["environmental_status"] ==
    "High Environmental Impact"
).sum()

moderate_impact_count = (
    filtered_df["environmental_status"] ==
    "Moderate Environmental Impact"
).sum()

low_impact_count = (
    filtered_df["environmental_status"] ==
    "Low Environmental Impact"
).sum()


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="live-badge">
            ● CLIMATE IMPACT ANALYTICS
        </div>

        <div class="hero-title">
            Climate Impact Intelligence
        </div>

        <div class="hero-subtitle">
            Combine weather and air-quality indicators to
            understand environmental conditions through
            interactive climate-impact analysis.
        </div>

    </div>

</div>
""")


# ============================================================
# OVERALL KPI
# ============================================================

st.markdown("### 🌍 Climate Impact Snapshot")
st.caption(
    "Summary indicators calculated from the selected dataset period."
)

kpis = [
    ("🌡️", "Average Temperature", f"{avg_temp:.1f} °C"),
    ("🔥", "Maximum Temperature", f"{max_temp:.1f} °C"),
    ("🌫️", "Average European AQI", f"{avg_aqi:.1f}"),
    ("📈", "Maximum European AQI", f"{max_aqi:.1f}"),
    ("🌧️", "Total Rainfall", f"{total_rain:.1f} mm"),
    ("⚠️", "High-Impact Records", f"{high_impact_count}")
]

kpi_columns = st.columns(6)

for column, item in zip(kpi_columns, kpis):

    icon, label, value = item

    with column:
        html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                {icon}
            </div>

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {value}
            </div>

        </div>
        """)


# ============================================================
# IMPACT INDICATOR CARDS
# ============================================================

st.markdown("### 🎯 Environmental Indicators")

indicator_columns = st.columns(3)

indicator_data = [
    (
        "HEAT INDICATOR",
        latest["heat_indicator"],
        f"Latest temperature: {latest['temperature_2m']:.1f} °C"
    ),
    (
        "RAINFALL INDICATOR",
        latest["rainfall_indicator"],
        f"Latest precipitation: {latest['precipitation']:.1f} mm"
    ),
    (
        "AIR POLLUTION INDICATOR",
        latest["air_pollution_indicator"],
        f"Latest European AQI: {latest['european_aqi']:.1f}"
    )
]

for column, item in zip(indicator_columns, indicator_data):

    label, status, detail = item

    with column:
        html(f"""
        <div class="impact-card">

            <div class="impact-label">
                {label}
            </div>

            <div class="impact-status">
                {status}
            </div>

            <div class="impact-detail">
                {detail}
            </div>

        </div>
        """)


# ============================================================
# ENVIRONMENTAL STATUS
# ============================================================

st.markdown("### 🌎 Overall Environmental Status")

status_counts = (
    filtered_df["environmental_status"]
    .value_counts()
    .reindex(
        [
            "Low Environmental Impact",
            "Moderate Environmental Impact",
            "High Environmental Impact"
        ],
        fill_value=0
    )
)

status_fig = go.Figure()

status_fig.add_trace(
    go.Bar(
        x=status_counts.index,
        y=status_counts.values,
        text=status_counts.values,
        textposition="auto"
    )
)

status_fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=25, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title="Environmental Status",
        showgrid=False
    ),
    yaxis=dict(
        title="Number of Records",
        gridcolor="rgba(255,255,255,0.07)"
    ),
    font=dict(color="#b9c8d8")
)

st.plotly_chart(
    status_fig,
    use_container_width=True
)


# ============================================================
# IMPACT TREND
# ============================================================

st.markdown("### 📈 Climate Impact Trend")

trend_df = (
    filtered_df
    .set_index("time")
    .resample("D")
    .agg(
        temperature=("temperature_2m", "mean"),
        aqi=("european_aqi", "mean"),
        rainfall=("precipitation", "sum")
    )
    .reset_index()
)

trend_metric = st.selectbox(
    "Trend metric",
    [
        "Temperature",
        "European AQI",
        "Rainfall"
    ],
    key="impact_trend_metric"
)

trend_mapping = {
    "Temperature": ("temperature", "Average Temperature (°C)"),
    "European AQI": ("aqi", "Average European AQI"),
    "Rainfall": ("rainfall", "Daily Rainfall (mm)")
}

trend_column, trend_label = trend_mapping[trend_metric]

fig_trend = px.area(
    trend_df,
    x="time",
    y=trend_column,
    labels={
        trend_column: trend_label,
        "time": ""
    }
)

fig_trend.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(
        title=trend_label,
        gridcolor="rgba(255,255,255,0.07)"
    ),
    hovermode="x unified",
    font=dict(color="#b9c8d8")
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.markdown("### 🔗 Climate Variable Correlation")

correlation_columns = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "pm2_5",
    "pm10",
    "carbon_dioxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "european_aqi"
]

available_correlation_columns = [
    col for col in correlation_columns
    if col in filtered_df.columns
]

if len(available_correlation_columns) >= 2:

    correlation_matrix = filtered_df[
        available_correlation_columns
    ].corr()

    correlation_matrix = correlation_matrix.rename(
        columns={
            "temperature_2m": "Temperature",
            "relative_humidity_2m": "Humidity",
            "precipitation": "Rainfall",
            "wind_speed_10m": "Wind Speed",
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "carbon_dioxide": "CO₂",
            "nitrogen_dioxide": "NO₂",
            "sulphur_dioxide": "SO₂",
            "ozone": "O₃",
            "european_aqi": "AQI"
        },
        index={
            "temperature_2m": "Temperature",
            "relative_humidity_2m": "Humidity",
            "precipitation": "Rainfall",
            "wind_speed_10m": "Wind Speed",
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "carbon_dioxide": "CO₂",
            "nitrogen_dioxide": "NO₂",
            "sulphur_dioxide": "SO₂",
            "ozone": "O₃",
            "european_aqi": "AQI"
        }
    )

    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        labels={
            "color": "Correlation"
        }
    )

    fig_corr.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

    st.caption(
        "Correlation shows statistical association between variables; "
        "it does not establish causation."
    )


# ============================================================
# TEMPERATURE VS PM2.5
# ============================================================

st.markdown("### 🌡️ Temperature vs PM2.5")

fig_scatter = px.scatter(
    filtered_df,
    x="temperature_2m",
    y="pm2_5",
    size="european_aqi",
    hover_data=[
        "time",
        "pm10",
        "european_aqi"
    ],
    labels={
        "temperature_2m": "Temperature (°C)",
        "pm2_5": "PM2.5 (µg/m³)",
        "european_aqi": "European AQI"
    }
)

fig_scatter.update_layout(
    height=440,
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.07)"
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.07)"
    ),
    font=dict(color="#b9c8d8")
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# IMPACT DISTRIBUTION
# ============================================================

st.markdown("### 📊 Indicator Distribution")

distribution_left, distribution_right = st.columns(2)

with distribution_left:

    heat_counts = (
        filtered_df["heat_indicator"]
        .value_counts()
        .reset_index()
    )

    heat_counts.columns = [
        "Heat Indicator",
        "Records"
    ]

    fig_heat = px.bar(
        heat_counts,
        x="Heat Indicator",
        y="Records",
        labels={
            "Heat Indicator": "",
            "Records": "Number of Records"
        }
    )

    fig_heat.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        ),
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )


with distribution_right:

    pollution_counts = (
        filtered_df["air_pollution_indicator"]
        .value_counts()
        .reset_index()
    )

    pollution_counts.columns = [
        "Air Pollution Indicator",
        "Records"
    ]

    fig_pollution = px.bar(
        pollution_counts,
        x="Air Pollution Indicator",
        y="Records",
        labels={
            "Air Pollution Indicator": "",
            "Records": "Number of Records"
        }
    )

    fig_pollution.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        ),
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_pollution,
        use_container_width=True
    )


# ============================================================
# ANALYTICAL SUMMARY
# ============================================================

st.markdown("### 💡 Impact Summary")

summary_columns = st.columns(3)

summary_items = [
    (
        "HIGH-IMPACT OBSERVATIONS",
        f"{high_impact_count}",
        "Records classified as high environmental impact by the project rules."
    ),
    (
        "MODERATE-IMPACT OBSERVATIONS",
        f"{moderate_impact_count}",
        "Records classified as moderate environmental impact."
    ),
    (
        "LOW-IMPACT OBSERVATIONS",
        f"{low_impact_count}",
        "Records classified as low environmental impact."
    )
]

for column, item in zip(summary_columns, summary_items):

    label, value, detail = item

    with column:
        html(f"""
        <div class="insight-card">

            <div class="insight-label">
                {label}
            </div>

            <div class="insight-value">
                {value}
            </div>

            <div class="insight-detail">
                {detail}
            </div>

        </div>
        """)


# ============================================================
# DATA TABLE
# ============================================================

st.markdown("### 📋 Climate Impact Records")

display_columns = [
    "time",
    "temperature_2m",
    "precipitation",
    "pm2_5",
    "pm10",
    "european_aqi",
    "heat_indicator",
    "rainfall_indicator",
    "air_pollution_indicator",
    "environmental_status"
]

available_columns = [
    col for col in display_columns
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[
        available_columns
    ]
    .tail(30)
    .sort_values("time", ascending=False),
    use_container_width=True,
    height=430
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Climate Impact Data",
    data=csv_data,
    file_name="climate_impact_analysis_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">

    <div style="
        font-size:18px;
        font-weight:800;
        color:#eaf4ff;
        margin-bottom:8px;
    ">
        🌍 Live Climate Impact Dashboard
    </div>

    <div style="
        font-size:14px;
        color:#a9bbce;
        margin-bottom:14px;
    ">
        Designed & Developed by
        <b style="color:#f3f8fd;">Sandesh Adhikari</b>
    </div>

    <div style="
        font-size:12px;
        color:#8297aa;
        line-height:2;
    ">
        Data Analyst Portfolio Project
        <br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>

    <div style="
        margin-top:16px;
        font-size:13px;
        line-height:2;
    ">

        <a href="mailto:adhikarisandesh333@gmail.com"
           style="color:#7ddff0; text-decoration:none; margin:0 10px;">
           📧 Email
        </a>

        <span style="color:#42566a;">|</span>

        <a href="https://github.com/sandeshadhikari1"
           target="_blank"
           style="color:#7ddff0; text-decoration:none; margin:0 10px;">
           💻 GitHub
        </a>

        <span style="color:#42566a;">|</span>

        <a href="https://www.linkedin.com/in/sandesh-adh/"
           target="_blank"
           style="color:#7ddff0; text-decoration:none; margin:0 10px;">
           🔗 LinkedIn
        </a>

        <span style="color:#42566a;">|</span>

        <a href="https://sandeshadhikari.info.np"
           target="_blank"
           style="color:#7ddff0; text-decoration:none; margin:0 10px;">
           🌐 Portfolio
        </a>

    </div>

    <div style="
        margin-top:18px;
        padding-top:14px;
        border-top:1px solid rgba(255,255,255,0.07);
        color:#657b90;
        font-size:11px;
    ">
        © 2026 Sandesh Adhikari • Climate & Environmental Data Analysis
    </div>

</div>
""")
