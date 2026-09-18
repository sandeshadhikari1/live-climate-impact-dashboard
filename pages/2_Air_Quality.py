import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Air Quality | Climate Intelligence",
    page_icon="🌫️",
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
    max-width: 900px;
    color: #a9bbce;
    font-size: 16px;
    line-height: 1.7;
}

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

.status-card {
    min-height: 125px;
    padding: 22px;
    border-radius: 18px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 30px rgba(0,0,0,0.16);
}

.status-label {
    color: #7890a5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.status-value {
    color: #f3f8fd;
    font-size: 25px;
    font-weight: 760;
    margin-bottom: 7px;
}

.status-detail {
    color: #8297aa;
    font-size: 13px;
}

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

.stButton > button,
.stDownloadButton button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(135deg, #11677c, #315d98);
    color: white;
    font-weight: 700;
}

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

    st.markdown("### 🌫️ Air Quality")

    st.caption(
        "Explore AQI, particulate matter, and atmospheric pollutants."
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
            key="air_start_date"
        )

    with date_columns[1]:
        end_date = st.date_input(
            "To",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="air_end_date"
        )

    st.markdown("### 📊 Pollutant")

    pollutant = st.selectbox(
        "Pollutant",
        [
            "PM2.5",
            "PM10",
            "Nitrogen Dioxide",
            "Sulphur Dioxide",
            "Ozone",
            "Carbon Monoxide",
            "Carbon Dioxide"
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
        <b>AIR QUALITY DATA</b><br>
        🛰️ Open-Meteo Air Quality API<br><br>

        <b>MONITORED</b><br>
        🟢 PM2.5 / PM10<br>
        🟢 European AQI<br>
        🟢 Gases & pollutants
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
    st.warning("No air-quality data is available for this period.")
    st.stop()


latest = filtered_df.iloc[-1]


# ============================================================
# COLUMN MAPPING
# ============================================================

pollutant_columns = {
    "PM2.5": ("pm2_5", "PM2.5 (µg/m³)"),
    "PM10": ("pm10", "PM10 (µg/m³)"),
    "Nitrogen Dioxide": ("nitrogen_dioxide", "NO₂ (µg/m³)"),
    "Sulphur Dioxide": ("sulphur_dioxide", "SO₂ (µg/m³)"),
    "Ozone": ("ozone", "O₃ (µg/m³)"),
    "Carbon Monoxide": ("carbon_monoxide", "CO (µg/m³)"),
    "Carbon Dioxide": ("carbon_dioxide", "CO₂ (µg/m³)")
}

pollutant_column, pollutant_label = pollutant_columns[pollutant]


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="live-badge">
            ● AIR QUALITY ANALYTICS
        </div>

        <div class="hero-title">
            Air Quality Intelligence
        </div>

        <div class="hero-subtitle">
            Monitor particulate matter, air-quality index,
            and atmospheric pollutants through interactive
            environmental analytics.
        </div>

    </div>

</div>
""")


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("### 🌫️ Air Quality Snapshot")
st.caption(
    "Key air-quality statistics for the selected analysis period."
)

avg_pm25 = filtered_df["pm2_5"].mean()
max_pm25 = filtered_df["pm2_5"].max()

avg_pm10 = filtered_df["pm10"].mean()
max_pm10 = filtered_df["pm10"].max()

avg_aqi = filtered_df["european_aqi"].mean()
max_aqi = filtered_df["european_aqi"].max()


kpis = [
    ("🌫️", "Average PM2.5", f"{avg_pm25:.1f} µg/m³"),
    ("🔴", "Maximum PM2.5", f"{max_pm25:.1f} µg/m³"),
    ("💨", "Average PM10", f"{avg_pm10:.1f} µg/m³"),
    ("📈", "Maximum PM10", f"{max_pm10:.1f} µg/m³"),
    ("📊", "Average European AQI", f"{avg_aqi:.1f}"),
    ("⚠️", "Maximum European AQI", f"{max_aqi:.1f}")
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
# CURRENT AIR QUALITY STATUS
# ============================================================

st.markdown("### 🌍 Current Air Quality Status")

current_aqi = latest["european_aqi"]

if pd.isna(current_aqi):
    aqi_status = "Unknown"
elif current_aqi <= 20:
    aqi_status = "Good"
elif current_aqi <= 40:
    aqi_status = "Fair"
elif current_aqi <= 60:
    aqi_status = "Moderate"
elif current_aqi <= 80:
    aqi_status = "Poor"
elif current_aqi <= 100:
    aqi_status = "Very Poor"
else:
    aqi_status = "Extremely Poor"


status_columns = st.columns(3)

statuses = [
    (
        "EUROPEAN AQI",
        aqi_status,
        (
            f"Latest AQI: {current_aqi:.1f}"
            if not pd.isna(current_aqi)
            else "AQI unavailable"
        )
    ),
    (
        "PM2.5",
        f"{latest['pm2_5']:.1f} µg/m³",
        "Latest fine particulate matter concentration."
    ),
    (
        "PM10",
        f"{latest['pm10']:.1f} µg/m³",
        "Latest coarse particulate matter concentration."
    )
]

for column, item in zip(status_columns, statuses):

    title, value, detail = item

    with column:
        html(f"""
        <div class="status-card">

            <div class="status-label">
                {title}
            </div>

            <div class="status-value">
                {value}
            </div>

            <div class="status-detail">
                {detail}
            </div>

        </div>
        """)


# ============================================================
# AQI GAUGE + POLLUTANT TREND
# ============================================================

st.markdown("### 📊 Air Quality Monitor")

left, right = st.columns(2)

with left:

    gauge_value = (
        float(current_aqi)
        if not pd.isna(current_aqi)
        else 0
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            title={"text": "European AQI"},
            gauge={
                "axis": {"range": [0, 120]},
                "bar": {"thickness": 0.25},
                "steps": [
                    {"range": [0, 20]},
                    {"range": [20, 40]},
                    {"range": [40, 60]},
                    {"range": [60, 80]},
                    {"range": [80, 100]},
                    {"range": [100, 120]}
                ],
                "threshold": {
                    "line": {"width": 4},
                    "value": gauge_value
                }
            }
        )
    )

    gauge.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )


with right:

    fig_pollutant = px.area(
        filtered_df,
        x="time",
        y=pollutant_column,
        labels={
            pollutant_column: pollutant_label,
            "time": ""
        }
    )

    fig_pollutant.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title=pollutant_label,
            gridcolor="rgba(255,255,255,0.07)"
        ),
        hovermode="x unified",
        font=dict(color="#b9c8d8")
    )

    st.plotly_chart(
        fig_pollutant,
        use_container_width=True
    )


# ============================================================
# PARTICULATE MATTER
# ============================================================

st.markdown("### 🌫️ Particulate Matter Analysis")

fig_pm = px.line(
    filtered_df,
    x="time",
    y=["pm2_5", "pm10"],
    labels={
        "value": "Concentration (µg/m³)",
        "time": "",
        "variable": "Pollutant"
    }
)

fig_pm.update_layout(
    height=440,
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
    fig_pm,
    use_container_width=True
)


# ============================================================
# POLLUTANT COMPARISON
# ============================================================

st.markdown("### 🧪 Atmospheric Pollutant Comparison")

pollutant_summary = pd.DataFrame({
    "Pollutant": [
        "PM2.5",
        "PM10",
        "CO",
        "CO₂",
        "NO₂",
        "SO₂",
        "O₃"
    ],
    "Average": [
        filtered_df["pm2_5"].mean(),
        filtered_df["pm10"].mean(),
        filtered_df["carbon_monoxide"].mean(),
        filtered_df["carbon_dioxide"].mean(),
        filtered_df["nitrogen_dioxide"].mean(),
        filtered_df["sulphur_dioxide"].mean(),
        filtered_df["ozone"].mean()
    ]
})

fig_comparison = px.bar(
    pollutant_summary,
    x="Pollutant",
    y="Average",
    labels={
        "Average": "Average Concentration",
        "Pollutant": ""
    }
)

fig_comparison.update_layout(
    height=430,
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
    fig_comparison,
    use_container_width=True
)


# ============================================================
# AQI + WEATHER RELATION
# ============================================================

st.markdown("### 🌡️ AQI & Temperature Relationship")

if "temperature_2m" in filtered_df.columns:

    fig_relation = px.scatter(
        filtered_df,
        x="temperature_2m",
        y="european_aqi",
        size="pm2_5",
        hover_data=["time", "pm10"],
        labels={
            "temperature_2m": "Temperature (°C)",
            "european_aqi": "European AQI",
            "pm2_5": "PM2.5"
        }
    )

    fig_relation.update_layout(
        height=430,
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
        fig_relation,
        use_container_width=True
    )


# ============================================================
# AQI HEATMAP
# ============================================================

st.markdown("### 🕐 AQI Pattern by Hour")

heatmap_df = filtered_df.copy()

heatmap_df["hour"] = heatmap_df["time"].dt.hour
heatmap_df["date"] = heatmap_df["time"].dt.date

aqi_heatmap = heatmap_df.pivot_table(
    index="hour",
    columns="date",
    values="european_aqi",
    aggfunc="mean"
)

if not aqi_heatmap.empty:

    fig_heatmap = px.imshow(
        aqi_heatmap,
        aspect="auto",
        labels={
            "x": "Date",
            "y": "Hour of Day",
            "color": "European AQI"
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
# AIR QUALITY DATA
# ============================================================

st.markdown("### 📋 Air Quality Observations")

display_columns = [
    "time",
    "pm2_5",
    "pm10",
    "european_aqi",
    "carbon_monoxide",
    "carbon_dioxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone"
]

available_columns = [
    col for col in display_columns
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns]
    .tail(20)
    .sort_values("time", ascending=False),
    use_container_width=True,
    height=380
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Air Quality Data",
    data=csv_data,
    file_name="air_quality_analysis_data.csv",
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