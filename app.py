import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Climate Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    """
    Render HTML directly instead of passing it through
    Streamlit Markdown.
    """
    st.html(content)


# ============================================================
# CUSTOM CSS
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


/* Hide default Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* Main page */

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

    border-right:
        1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #dce8f5;
}


/* Hero */

.hero {
    position: relative;

    padding: 42px;

    border-radius: 26px;

    background:
        linear-gradient(
            135deg,
            rgba(20,105,130,0.45),
            rgba(55,48,120,0.40)
        );

    border:
        1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.35);

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

    background:
        rgba(50,200,220,0.16);

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

    background:
        rgba(50,220,170,0.10);

    border:
        1px solid rgba(50,220,170,0.30);

    color: #63e6b8;

    font-size: 12px;

    font-weight: 750;

    letter-spacing: 1px;

    margin-bottom: 16px;
}


.hero-title {
    font-size: 46px;

    font-weight: 800;

    letter-spacing: -2px;

    line-height: 1.1;

    color: #f6faff;

    margin-bottom: 14px;
}


.hero-subtitle {
    max-width: 850px;

    color: #a9bbce;

    font-size: 16px;

    line-height: 1.7;
}


/* Section title */

.section-title {
    font-size: 23px;

    font-weight: 750;

    color: #f2f7fd;

    margin-top: 30px;

    margin-bottom: 16px;
}


.section-description {
    color: #8196ab;

    font-size: 14px;

    margin-top: -8px;

    margin-bottom: 18px;
}


/* KPI */

.kpi-card {
    min-height: 140px;

    padding: 22px;

    border-radius: 19px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );

    border:
        1px solid rgba(255,255,255,0.09);

    box-shadow:
        0 15px 35px rgba(0,0,0,0.20);

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


/* Status cards */

.status-card {
    min-height: 125px;

    padding: 22px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 12px 30px rgba(0,0,0,0.16);
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


/* Sidebar branding */

.sidebar-title {
    color: #f4f8ff;

    font-size: 24px;

    font-weight: 800;
}


.sidebar-subtitle {
    color: #738aa0;

    font-size: 12px;

    margin-top: 5px;

    margin-bottom: 25px;
}


.sidebar-status {
    padding: 15px;

    border-radius: 14px;

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.07);

    color: #8196aa;

    font-size: 12px;

    line-height: 1.9;
}


/* Buttons */

.stButton > button {
    border-radius: 12px;

    border:
        1px solid rgba(255,255,255,0.12);

    background:
        linear-gradient(
            135deg,
            #11677c,
            #315d98
        );

    color: white;

    font-weight: 700;
}


.stDownloadButton button {
    border-radius: 12px;

    border:
        1px solid rgba(255,255,255,0.12);

    background:
        linear-gradient(
            135deg,
            #11677c,
            #315d98
        );

    color: white;

    font-weight: 700;
}


/* Selectbox */

div[data-baseweb="select"] > div {
    background:
        rgba(255,255,255,0.055);

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius: 11px;
}


/* Date input */

div[data-testid="stDateInput"] input {
    background:
        rgba(255,255,255,0.055);

    color: white;

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius: 10px;
}


/* Expander */

div[data-testid="stExpander"] {
    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 14px;

    background:
        rgba(255,255,255,0.025);
}


/* Footer */

.footer {
    margin-top: 50px;

    padding-top: 25px;

    border-top:
        1px solid rgba(255,255,255,0.07);

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

    df = pd.read_csv(
        "data/climate_history_cleaned.csv"
    )

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["time"]
    )

    df = df.sort_values(
        "time"
    ).reset_index(drop=True)

    return df


try:

    climate_df = load_data()

except FileNotFoundError:

    st.error(
        "❌ climate_history_cleaned.csv was not found."
    )

    st.info(
        "Make sure the file is inside: "
        "data/climate_history_cleaned.csv"
    )

    st.stop()


if climate_df.empty:

    st.error(
        "The climate dataset is empty."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div class="sidebar-title">
        🌍 Climate Intelligence
    </div>

    <div class="sidebar-subtitle">
        Environmental Monitoring Platform
    </div>
    """)


    st.markdown("### 📅 Analysis Period")


    min_date = climate_df["time"].min().date()

    max_date = climate_df["time"].max().date()


    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )


    st.markdown("### 📊 Primary Metric")


    metric = st.selectbox(
        "Metric",
        [
            "Temperature",
            "PM2.5",
            "PM10",
            "European AQI",
            "Rainfall"
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
    <div class="sidebar-status">

        <b>DATA SOURCES</b>

        <br>

        🛰️ Open-Meteo Weather API

        <br>

        🌫️ Open-Meteo Air Quality API

        <br><br>

        <b>PIPELINE STATUS</b>

        <br>

        🟢 Data available

        <br>

        🟢 Visualization active

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

    end_time = climate_df["time"].max()

    start_time = (
        end_time
        - pd.Timedelta(days=days)
    )

    filtered_df = climate_df[
        (climate_df["time"] >= start_time)
        &
        (climate_df["time"] <= end_time)
    ].copy()

else:

    if (
        isinstance(date_range, tuple)
        and len(date_range) == 2
    ):

        start_date = pd.Timestamp(
            date_range[0]
        )

        end_date = (
            pd.Timestamp(date_range[1])
            + pd.Timedelta(days=1)
        )

        filtered_df = climate_df[
            (climate_df["time"] >= start_date)
            &
            (climate_df["time"] < end_date)
        ].copy()

    else:

        filtered_df = climate_df.copy()


if filtered_df.empty:

    st.warning(
        "No data is available for this period."
    )

    st.stop()


# ============================================================
# LATEST DATA
# ============================================================

latest = filtered_df.iloc[-1]


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="live-badge">
            ● LIVE CLIMATE MONITORING
        </div>

        <div class="hero-title">
            Climate Intelligence Dashboard
        </div>

        <div class="hero-subtitle">
            Explore atmospheric conditions, air quality,
            rainfall patterns, and environmental indicators
            through interactive climate analytics.
        </div>

    </div>

</div>
""")


# ============================================================
# KPI CALCULATIONS
# ============================================================

avg_temp = filtered_df[
    "temperature_2m"
].mean()

max_temp = filtered_df[
    "temperature_2m"
].max()

avg_pm25 = filtered_df[
    "pm2_5"
].mean()

avg_pm10 = filtered_df[
    "pm10"
].mean()

avg_aqi = filtered_df[
    "european_aqi"
].mean()

total_rain = filtered_df[
    "precipitation"
].sum()


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    "### 📊 Climate Snapshot"
)


kpi_columns = st.columns(6)


kpis = [

    (
        "🌡️",
        "Average Temperature",
        f"{avg_temp:.1f} °C"
    ),

    (
        "🔥",
        "Maximum Temperature",
        f"{max_temp:.1f} °C"
    ),

    (
        "🌫️",
        "Average PM2.5",
        f"{avg_pm25:.1f} µg/m³"
    ),

    (
        "💨",
        "Average PM10",
        f"{avg_pm10:.1f} µg/m³"
    ),

    (
        "📊",
        "Average AQI",
        f"{avg_aqi:.1f}"
    ),

    (
        "🌧️",
        "Total Rainfall",
        f"{total_rain:.1f} mm"
    )
]


for column, item in zip(
    kpi_columns,
    kpis
):

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
# ENVIRONMENT STATUS
# ============================================================

st.markdown(
    "### 🌍 Environmental Snapshot"
)


current_aqi = latest["european_aqi"]

current_temp = latest["temperature_2m"]

current_rain = latest["precipitation"]


# AQI

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


# Heat

if pd.isna(current_temp):

    heat_status = "Unknown"

elif current_temp < 25:

    heat_status = "Low"

elif current_temp < 30:

    heat_status = "Moderate"

elif current_temp < 35:

    heat_status = "High"

else:

    heat_status = "Very High"


# Rain

if pd.isna(current_rain):

    rain_status = "Unknown"

elif current_rain == 0:

    rain_status = "No Rain"

elif current_rain < 2.5:

    rain_status = "Light"

elif current_rain < 7.6:

    rain_status = "Moderate"

elif current_rain < 15:

    rain_status = "Heavy"

else:

    rain_status = "Very Heavy"


status_columns = st.columns(3)


statuses = [

    (
        "🌫️ AIR QUALITY",
        aqi_status,
        (
            f"European AQI: {current_aqi:.1f}"
            if not pd.isna(current_aqi)
            else "AQI unavailable"
        )
    ),

    (
        "🌡️ HEAT CONDITION",
        heat_status,
        (
            f"Temperature: {current_temp:.1f} °C"
            if not pd.isna(current_temp)
            else "Temperature unavailable"
        )
    ),

    (
        "🌧️ RAINFALL",
        rain_status,
        (
            f"Current rainfall: {current_rain:.1f} mm"
            if not pd.isna(current_rain)
            else "Rainfall unavailable"
        )
    )
]


for column, item in zip(
    status_columns,
    statuses
):

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
# MAIN TREND
# ============================================================

st.markdown(
    "### 📈 Climate Trend Explorer"
)


st.caption(
    "Change the metric or analysis period from the sidebar."
)


metric_columns = {

    "Temperature": (
        "temperature_2m",
        "Temperature (°C)"
    ),

    "PM2.5": (
        "pm2_5",
        "PM2.5 (µg/m³)"
    ),

    "PM10": (
        "pm10",
        "PM10 (µg/m³)"
    ),

    "European AQI": (
        "european_aqi",
        "European AQI"
    ),

    "Rainfall": (
        "precipitation",
        "Rainfall (mm)"
    )
}


column_name, y_label = metric_columns[
    metric
]


fig_trend = px.area(
    filtered_df,
    x="time",
    y=column_name
)


fig_trend.update_layout(
    height=480,

    margin=dict(
        l=20,
        r=20,
        t=25,
        b=20
    ),

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

    font=dict(
        color="#b9c8d8"
    )
)


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# TEMPERATURE HEATMAP
# ============================================================

st.markdown(
    "### 🌡️ Temperature Heatmap"
)


if "hour" not in filtered_df.columns:

    filtered_df["hour"] = (
        filtered_df["time"].dt.hour
    )


filtered_df["date"] = (
    filtered_df["time"].dt.date
)


temperature_heatmap = filtered_df.pivot_table(
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
            "y": "Hour",
            "color": "Temperature"
        }
    )


    fig_heatmap.update_layout(
        height=480,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )


# ============================================================
# ATMOSPHERIC CONDITIONS
# ============================================================

st.markdown(
    "### 🌫️ Atmospheric Conditions"
)


left, right = st.columns(2)


with left:

    fig_pm = px.area(
        filtered_df,
        x="time",
        y=[
            "pm2_5",
            "pm10"
        ]
    )


    fig_pm.update_layout(
        height=430,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        hovermode="x unified"
    )


    st.plotly_chart(
        fig_pm,
        use_container_width=True
    )


with right:

    fig_rain = px.bar(
        filtered_df,
        x="time",
        y="precipitation"
    )


    fig_rain.update_layout(
        height=430,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        hovermode="x unified"
    )


    st.plotly_chart(
        fig_rain,
        use_container_width=True
    )


# ============================================================
# ENVIRONMENTAL ANALYTICS
# ============================================================

st.markdown(
    "### 🔬 Environmental Analytics"
)


left, right = st.columns(2)


# AQI Gauge

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

            title={
                "text": "European AQI"
            },

            gauge={

                "axis": {
                    "range": [0, 120]
                },

                "bar": {
                    "thickness": 0.25
                },

                "steps": [

                    {"range": [0, 20]},

                    {"range": [20, 40]},

                    {"range": [40, 60]},

                    {"range": [60, 80]},

                    {"range": [80, 100]},

                    {"range": [100, 120]}
                ],

                "threshold": {

                    "line": {
                        "width": 4
                    },

                    "value": gauge_value
                }
            }
        )
    )


    gauge.update_layout(
        height=430,

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        gauge,
        use_container_width=True
    )


# Temperature / PM2.5

with right:

    fig_scatter = px.scatter(
        filtered_df,
        x="temperature_2m",
        y="pm2_5",
        size="european_aqi",
        hover_data=[
            "time",
            "pm10"
        ],
        labels={
            "temperature_2m":
                "Temperature (°C)",

            "pm2_5":
                "PM2.5 (µg/m³)",

            "european_aqi":
                "AQI"
        }
    )


    fig_scatter.update_layout(
        height=430,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)"
        )
    )


    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    "### 📊 Data Explorer"
)


with st.expander(
    "🔎 Open interactive climate dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Filtered Climate Data",
    data=csv_data,
    file_name="climate_data_filtered.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">

    <b>🌍 Climate Intelligence Dashboard</b>

    <br>

    Interactive Climate & Environmental Analytics

    <br><br>

    Built with Python • Pandas • Plotly • Streamlit

    <br>

    Weather & Air Quality data powered by Open-Meteo

</div>
""")