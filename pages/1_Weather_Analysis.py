import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Weather Analysis | Climate Intelligence",
    page_icon="🌡️",
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
        radial-gradient(
            circle at 0% 0%,
            rgba(0, 190, 220, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 100% 0%,
            rgba(100, 70, 200, 0.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #06111f,
            #0a1627 50%,
            #0d1423
        );
    color: #eef6ff;
}

#MainMenu,
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Keep native sidebar/menu control visible and blended */
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

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #06111f,
            #07101c
        );
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
    background:
        linear-gradient(
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
    max-width: 900px;
    color: #a9bbce;
    font-size: 16px;
    line-height: 1.7;
}

/* Section titles */
.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #f2f7fd;
    margin-top: 30px;
    margin-bottom: 8px;
}

.section-description {
    color: #8196ab;
    font-size: 14px;
    margin-bottom: 18px;
}

/* KPI */
.kpi-card {
    min-height: 145px;
    padding: 22px;
    border-radius: 19px;
    background:
        linear-gradient(
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

/* Insight cards */
.insight-card {
    min-height: 120px;
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
    background:
        linear-gradient(
            135deg,
            #11677c,
            #315d98
        );
    color: white;
    font-weight: 700;
}

/* Dataframe / expander */
div[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    background: rgba(255,255,255,0.025);
}

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

    st.markdown("### 🌡️ Weather Analysis")

    st.caption(
        "Explore temperature, humidity, rainfall, and wind patterns."
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
            key="weather_start_date"
        )

    with date_columns[1]:
        end_date = st.date_input(
            "To",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="weather_end_date"
        )

    st.markdown("### 📊 Main Metric")

    weather_metric = st.selectbox(
        "Metric",
        [
            "Temperature",
            "Feels Like Temperature",
            "Humidity",
            "Rainfall",
            "Wind Speed"
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
        <b>WEATHER DATA</b><br>
        🛰️ Open-Meteo Weather API<br><br>

        <b>ANALYTICS</b><br>
        🟢 Temperature<br>
        🟢 Humidity<br>
        🟢 Rainfall<br>
        🟢 Wind
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
    st.warning("No weather data is available for this period.")
    st.stop()


latest = filtered_df.iloc[-1]


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="live-badge">
            ● WEATHER ANALYTICS
        </div>

        <div class="hero-title">
            Weather Analysis
        </div>

        <div class="hero-subtitle">
            Analyze temperature, humidity, rainfall, and wind
            conditions through interactive weather analytics
            and time-based visualizations.
        </div>

    </div>

</div>
""")


# ============================================================
# CURRENT WEATHER KPIs
# ============================================================

st.markdown("### 🌤️ Weather Snapshot")
st.caption(
    "Key weather statistics for the selected analysis period."
)

avg_temp = filtered_df["temperature_2m"].mean()
max_temp = filtered_df["temperature_2m"].max()
min_temp = filtered_df["temperature_2m"].min()

avg_humidity = filtered_df["relative_humidity_2m"].mean()

total_rain = filtered_df["precipitation"].sum()

avg_wind = filtered_df["wind_speed_10m"].mean()
max_wind = filtered_df["wind_speed_10m"].max()


kpis = [
    ("🌡️", "Average Temperature", f"{avg_temp:.1f} °C"),
    ("🔥", "Maximum Temperature", f"{max_temp:.1f} °C"),
    ("❄️", "Minimum Temperature", f"{min_temp:.1f} °C"),
    ("💧", "Average Humidity", f"{avg_humidity:.1f} %"),
    ("🌧️", "Total Rainfall", f"{total_rain:.1f} mm"),
    ("💨", "Maximum Wind", f"{max_wind:.1f} km/h")
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
# QUICK WEATHER INSIGHTS
# ============================================================

st.markdown("### 🔎 Weather Insights")

insight_columns = st.columns(3)

temp_range = max_temp - min_temp

rain_days = (
    filtered_df["precipitation"] > 0
).sum()

wind_direction = latest.get(
    "wind_direction_10m",
    float("nan")
)

if pd.isna(wind_direction):
    wind_text = "Unavailable"
else:
    wind_text = f"{wind_direction:.0f}°"


insights = [
    (
        "TEMPERATURE RANGE",
        f"{temp_range:.1f} °C",
        f"Difference between the lowest and highest recorded temperature."
    ),
    (
        "RAINY OBSERVATIONS",
        f"{rain_days}",
        f"Time records with measurable precipitation in the selected period."
    ),
    (
        "LATEST WIND DIRECTION",
        wind_text,
        "Wind direction in degrees from the latest available observation."
    )
]

for column, item in zip(insight_columns, insights):

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
# MAIN WEATHER TREND
# ============================================================

st.markdown("### 📈 Weather Trend Explorer")

metric_columns = {
    "Temperature": (
        "temperature_2m",
        "Temperature (°C)"
    ),
    "Feels Like Temperature": (
        "apparent_temperature",
        "Feels Like Temperature (°C)"
    ),
    "Humidity": (
        "relative_humidity_2m",
        "Relative Humidity (%)"
    ),
    "Rainfall": (
        "precipitation",
        "Rainfall (mm)"
    ),
    "Wind Speed": (
        "wind_speed_10m",
        "Wind Speed (km/h)"
    )
}

column_name, y_label = metric_columns[weather_metric]

fig_trend = px.area(
    filtered_df,
    x="time",
    y=column_name,
    labels={
        column_name: y_label,
        "time": ""
    }
)

fig_trend.update_layout(
    height=470,
    margin=dict(l=20, r=20, t=25, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title="",
        showgrid=False
    ),
    yaxis=dict(
        title=y_label,
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
# TEMPERATURE + HUMIDITY
# ============================================================

st.markdown("### 🌡️ Temperature & Humidity")

left, right = st.columns(2)

with left:

    fig_temp = px.line(
        filtered_df,
        x="time",
        y=[
            "temperature_2m",
            "apparent_temperature"
        ],
        labels={
            "value": "Temperature (°C)",
            "time": "",
            "variable": "Measure"
        }
    )

    fig_temp.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        ),
        hovermode="x unified",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )


with right:

    fig_humidity = px.area(
        filtered_df,
        x="time",
        y="relative_humidity_2m",
        labels={
            "relative_humidity_2m":
                "Relative Humidity (%)",
            "time": ""
        }
    )

    fig_humidity.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        ),
        hovermode="x unified",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_humidity,
        use_container_width=True
    )


# ============================================================
# RAINFALL + WIND
# ============================================================

st.markdown("### 🌧️ Rainfall & Wind")

left, right = st.columns(2)

with left:

    fig_rain = px.bar(
        filtered_df,
        x="time",
        y="precipitation",
        labels={
            "precipitation": "Rainfall (mm)",
            "time": ""
        }
    )

    fig_rain.update_layout(
        height=420,
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
        fig_rain,
        use_container_width=True
    )


with right:

    fig_wind = px.line(
        filtered_df,
        x="time",
        y="wind_speed_10m",
        labels={
            "wind_speed_10m": "Wind Speed (km/h)",
            "time": ""
        }
    )

    fig_wind.update_layout(
        height=420,
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
        fig_wind,
        use_container_width=True
    )


# ============================================================
# TEMPERATURE HEATMAP
# ============================================================

st.markdown("### 🕐 Temperature Pattern by Hour")

heatmap_df = filtered_df.copy()

heatmap_df["hour"] = heatmap_df["time"].dt.hour
heatmap_df["date"] = heatmap_df["time"].dt.date

temperature_heatmap = heatmap_df.pivot_table(
    index="hour",
    columns="date",
    values="temperature_2m",
    aggfunc="mean"
)

if not temperature_heatmap.empty:

    fig_heatmap = px.imshow(
        temperature_heatmap,
        aspect="auto",
        labels={
            "x": "Date",
            "y": "Hour of Day",
            "color": "Temperature (°C)"
        }
    )

    fig_heatmap.update_layout(
        height=480,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )


# ============================================================
# WEATHER DETAILS
# ============================================================

st.markdown("### 📋 Latest Weather Observation")

latest_columns = [
    "time",
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m"
]

available_columns = [
    col for col in latest_columns
    if col in filtered_df.columns
]

latest_display = (
    filtered_df[available_columns]
    .tail(10)
    .sort_values("time", ascending=False)
    .copy()
)

st.dataframe(
    latest_display,
    use_container_width=True,
    height=330
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Weather Data",
    data=csv_data,
    file_name="weather_analysis_data.csv",
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