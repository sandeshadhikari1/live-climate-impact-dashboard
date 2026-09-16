import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Air Quality Analysis",
    page_icon="🌫️",
    layout="wide"
)


# ==================================================
# LOCATION
# ==================================================

latitude = 27.7172
longitude = 85.3240


# ==================================================
# AIR QUALITY API
# ==================================================

def get_air_quality_data():

    air_url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
    )

    air_params = {

        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "carbon_dioxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "european_aqi"
        ],

        "hourly": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "carbon_dioxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "european_aqi"
        ],

        "timezone": "Asia/Kathmandu"
    }

    response = requests.get(
        air_url,
        params=air_params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# LOAD AIR QUALITY DATA
# ==================================================

try:

    air_data = get_air_quality_data()

    current = air_data["current"]

    hourly_df = pd.DataFrame(
        air_data["hourly"]
    )

    hourly_df["time"] = pd.to_datetime(
        hourly_df["time"]
    )

except Exception as e:

    st.error(
        f"Unable to collect air quality data: {e}"
    )

    st.stop()


# ==================================================
# TITLE
# ==================================================

st.title("🌫️ Air Quality Analysis")

st.write(
    "Monitor current air pollution levels and "
    "hourly air quality conditions in Kathmandu."
)

st.divider()


# ==================================================
# CURRENT AIR QUALITY
# ==================================================

st.subheader("🌫️ Current Air Quality")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "PM2.5",
        f"{current['pm2_5']:.1f} µg/m³"
    )


with col2:

    st.metric(
        "PM10",
        f"{current['pm10']:.1f} µg/m³"
    )


with col3:

    st.metric(
        "European AQI",
        f"{current['european_aqi']:.0f}"
    )


with col4:

    st.metric(
        "Ozone",
        f"{current['ozone']:.1f} µg/m³"
    )


st.divider()


# ==================================================
# AQI CATEGORY
# ==================================================

def aqi_category(aqi):

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


current_aqi_category = aqi_category(
    current["european_aqi"]
)


st.subheader("🟠 Air Quality Status")

st.info(
    f"Current European AQI Category: "
    f"**{current_aqi_category}**"
)


st.divider()


# ==================================================
# PM2.5 AND PM10
# ==================================================

st.subheader("📈 Particulate Matter Trends")

col1, col2 = st.columns(2)


with col1:

    fig_pm25 = px.line(
        hourly_df,
        x="time",
        y="pm2_5",
        title="PM2.5 Trend",
        labels={
            "time": "Time",
            "pm2_5": "PM2.5 (µg/m³)"
        }
    )

    st.plotly_chart(
        fig_pm25,
        use_container_width=True
    )


with col2:

    fig_pm10 = px.line(
        hourly_df,
        x="time",
        y="pm10",
        title="PM10 Trend",
        labels={
            "time": "Time",
            "pm10": "PM10 (µg/m³)"
        }
    )

    st.plotly_chart(
        fig_pm10,
        use_container_width=True
    )


# ==================================================
# AQI TREND
# ==================================================

st.subheader("🟠 European AQI Trend")

fig_aqi = px.line(
    hourly_df,
    x="time",
    y="european_aqi",
    title="European Air Quality Index",
    labels={
        "time": "Time",
        "european_aqi": "European AQI"
    }
)

st.plotly_chart(
    fig_aqi,
    use_container_width=True
)


# ==================================================
# POLLUTANT TRENDS
# ==================================================

st.subheader("🧪 Other Air Pollutants")

pollutant = st.selectbox(
    "Select pollutant",
    [
        "carbon_monoxide",
        "carbon_dioxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone"
    ]
)


fig_pollutant = px.line(
    hourly_df,
    x="time",
    y=pollutant,
    title=f"{pollutant.replace('_', ' ').title()} Trend",
    labels={
        "time": "Time",
        pollutant: "Concentration"
    }
)

st.plotly_chart(
    fig_pollutant,
    use_container_width=True
)


# ==================================================
# AIR QUALITY SUMMARY
# ==================================================

st.subheader("📊 Air Quality Summary")

summary_df = pd.DataFrame({

    "Pollutant": [
        "PM2.5",
        "PM10",
        "Carbon Monoxide",
        "Carbon Dioxide",
        "Nitrogen Dioxide",
        "Sulphur Dioxide",
        "Ozone"
    ],

    "Average": [
        hourly_df["pm2_5"].mean(),
        hourly_df["pm10"].mean(),
        hourly_df["carbon_monoxide"].mean(),
        hourly_df["carbon_dioxide"].mean(),
        hourly_df["nitrogen_dioxide"].mean(),
        hourly_df["sulphur_dioxide"].mean(),
        hourly_df["ozone"].mean()
    ],

    "Maximum": [
        hourly_df["pm2_5"].max(),
        hourly_df["pm10"].max(),
        hourly_df["carbon_monoxide"].max(),
        hourly_df["carbon_dioxide"].max(),
        hourly_df["nitrogen_dioxide"].max(),
        hourly_df["sulphur_dioxide"].max(),
        hourly_df["ozone"].max()
    ]
})


summary_df["Average"] = summary_df["Average"].round(2)
summary_df["Maximum"] = summary_df["Maximum"].round(2)


st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# HOURLY AIR QUALITY DATA
# ==================================================

st.subheader("📋 Hourly Air Quality Data")

st.dataframe(
    hourly_df,
    use_container_width=True,
    hide_index=True
)