import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Live Climate Impact Dashboard",
    page_icon="🌍",
    layout="wide"
)


# ==================================================
# LOCATION
# ==================================================

latitude = 27.7172
longitude = 85.3240
location_name = "Kathmandu"


# ==================================================
# LIVE DATA COLLECTION FUNCTION
# ==================================================

def collect_climate_data(latitude, longitude):

    # ----------------------------------------------
    # WEATHER API
    # ----------------------------------------------

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m"
        ],
        "timezone": "Asia/Kathmandu"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=30
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()


    # ----------------------------------------------
    # AIR QUALITY API
    # ----------------------------------------------

    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

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
        "timezone": "Asia/Kathmandu"
    }

    air_response = requests.get(
        air_url,
        params=air_params,
        timeout=30
    )

    air_response.raise_for_status()

    air_data = air_response.json()


    # ----------------------------------------------
    # COMBINE WEATHER + AIR QUALITY
    # ----------------------------------------------

    climate_data = {

        "timestamp": weather_data["current"]["time"],

        "temperature_2m":
            weather_data["current"]["temperature_2m"],

        "relative_humidity_2m":
            weather_data["current"]["relative_humidity_2m"],

        "apparent_temperature":
            weather_data["current"]["apparent_temperature"],

        "precipitation":
            weather_data["current"]["precipitation"],

        "wind_speed_10m":
            weather_data["current"]["wind_speed_10m"],

        "wind_direction_10m":
            weather_data["current"]["wind_direction_10m"],

        "pm10":
            air_data["current"]["pm10"],

        "pm2_5":
            air_data["current"]["pm2_5"],

        "carbon_monoxide":
            air_data["current"]["carbon_monoxide"],

        "carbon_dioxide":
            air_data["current"]["carbon_dioxide"],

        "nitrogen_dioxide":
            air_data["current"]["nitrogen_dioxide"],

        "sulphur_dioxide":
            air_data["current"]["sulphur_dioxide"],

        "ozone":
            air_data["current"]["ozone"],

        "european_aqi":
            air_data["current"]["european_aqi"],

        "collected_at":
            datetime.now()
    }


    return pd.DataFrame([climate_data])


# ==================================================
# CLIMATE INDICATORS
# ==================================================

def heat_indicator(temp):

    if temp < 25:
        return "Low"

    elif temp < 30:
        return "Moderate"

    elif temp < 35:
        return "High"

    else:
        return "Very High"


def rainfall_indicator(rain):

    if rain == 0:
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


# ==================================================
# GET LIVE DATA
# ==================================================

if "live_data" not in st.session_state:

    try:

        st.session_state.live_data = collect_climate_data(
            latitude,
            longitude
        )

    except Exception as e:

        st.error(
            f"Unable to collect live climate data: {e}"
        )

        st.stop()


climate_df = st.session_state.live_data.copy()


# ==================================================
# APPLY CLIMATE INDICATORS
# ==================================================

climate_df["heat_indicator"] = climate_df[
    "temperature_2m"
].apply(heat_indicator)


climate_df["rainfall_indicator"] = climate_df[
    "precipitation"
].apply(rainfall_indicator)


climate_df["air_pollution_indicator"] = climate_df[
    "european_aqi"
].apply(air_pollution_indicator)


climate_df["environmental_status"] = climate_df.apply(
    environmental_status,
    axis=1
)


# ==================================================
# TITLE
# ==================================================

st.title("🌍 Live Climate Impact Dashboard")

st.write(
    "Monitor current weather, air quality, and "
    "environmental conditions in Kathmandu."
)


st.divider()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Dashboard Controls")

st.sidebar.subheader("📍 Location")

st.sidebar.selectbox(
    "Select Location",
    ["Kathmandu"]
)


st.sidebar.subheader("🔄 Live Data")

if st.sidebar.button("Refresh Live Data"):

    try:

        with st.spinner("Collecting fresh climate data..."):

            new_data = collect_climate_data(
                latitude,
                longitude
            )

        st.session_state.live_data = new_data

        st.success("Live data updated successfully!")

        st.rerun()

    except Exception as e:

        st.error(
            f"Unable to refresh data: {e}"
        )


# ==================================================
# LATEST DATA
# ==================================================

latest = climate_df.iloc[0]


# ==================================================
# LAST UPDATED
# ==================================================

st.caption(
    f"Last API update: {latest['timestamp']} "
    f"| Collected by dashboard: "
    f"{latest['collected_at']}"
)


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("📊 Current Climate Conditions")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🌡️ Temperature",
        f"{latest['temperature_2m']:.1f} °C"
    )


with col2:

    st.metric(
        "💧 Humidity",
        f"{latest['relative_humidity_2m']:.1f}%"
    )


with col3:

    st.metric(
        "🌫️ PM2.5",
        f"{latest['pm2_5']:.1f} µg/m³"
    )


with col4:

    st.metric(
        "🟠 European AQI",
        f"{latest['european_aqi']:.0f}"
    )


with col5:

    st.metric(
        "🌧️ Rainfall",
        f"{latest['precipitation']:.1f} mm"
    )


st.divider()


# ==================================================
# ENVIRONMENTAL STATUS
# ==================================================

st.subheader("🌍 Environmental Status")

status = latest["environmental_status"]

st.info(
    f"Current Environmental Status: **{status}**"
)


# ==================================================
# CLIMATE INDICATORS
# ==================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔥 Heat Indicator",
        latest["heat_indicator"]
    )


with col2:

    st.metric(
        "🌧️ Rainfall Indicator",
        latest["rainfall_indicator"]
    )


with col3:

    st.metric(
        "🌫️ Air Pollution",
        latest["air_pollution_indicator"]
    )


st.divider()


# ==================================================
# WEATHER INFORMATION
# ==================================================

st.subheader("🌡️ Weather Information")

weather_display = pd.DataFrame({
    "Metric": [
        "Temperature",
        "Apparent Temperature",
        "Relative Humidity",
        "Precipitation",
        "Wind Speed",
        "Wind Direction"
    ],

    "Value": [
        f"{latest['temperature_2m']:.1f} °C",
        f"{latest['apparent_temperature']:.1f} °C",
        f"{latest['relative_humidity_2m']:.1f} %",
        f"{latest['precipitation']:.1f} mm",
        f"{latest['wind_speed_10m']:.1f} km/h",
        f"{latest['wind_direction_10m']:.0f}°"
    ]
})

st.dataframe(
    weather_display,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# AIR QUALITY INFORMATION
# ==================================================

st.subheader("🌫️ Air Quality Information")

air_display = pd.DataFrame({
    "Pollutant": [
        "PM2.5",
        "PM10",
        "Carbon Monoxide",
        "Carbon Dioxide",
        "Nitrogen Dioxide",
        "Sulphur Dioxide",
        "Ozone"
    ],

    "Value": [
        f"{latest['pm2_5']:.2f} µg/m³",
        f"{latest['pm10']:.2f} µg/m³",
        f"{latest['carbon_monoxide']:.2f} µg/m³",
        f"{latest['carbon_dioxide']:.2f} ppm",
        f"{latest['nitrogen_dioxide']:.2f} µg/m³",
        f"{latest['sulphur_dioxide']:.2f} µg/m³",
        f"{latest['ozone']:.2f} µg/m³"
    ]
})

st.dataframe(
    air_display,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# RAW LIVE DATA
# ==================================================

st.subheader("📋 Current Live Data")

st.dataframe(
    climate_df,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# CSV DOWNLOAD
# ==================================================

st.subheader("⬇️ Download Live Data")

csv_data = climate_df.to_csv(
    index=False
)

st.download_button(
    label="Download Current Climate Data",
    data=csv_data,
    file_name="live_climate_data.csv",
    mime="text/csv"
)