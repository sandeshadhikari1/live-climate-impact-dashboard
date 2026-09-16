import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Weather Analysis",
    page_icon="🌡️",
    layout="wide"
)


# ==================================================
# LOCATION
# ==================================================

latitude = 27.7172
longitude = 85.3240


# ==================================================
# GET WEATHER DATA
# ==================================================

def get_weather_data():

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

        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ],

        "timezone": "Asia/Kathmandu"
    }

    response = requests.get(
        weather_url,
        params=weather_params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# LOAD WEATHER DATA
# ==================================================

try:

    weather_data = get_weather_data()

    current = weather_data["current"]

    hourly_df = pd.DataFrame(
        weather_data["hourly"]
    )

    hourly_df["time"] = pd.to_datetime(
        hourly_df["time"]
    )

except Exception as e:

    st.error(
        f"Unable to collect weather data: {e}"
    )

    st.stop()


# ==================================================
# TITLE
# ==================================================

st.title("🌡️ Weather Analysis")

st.write(
    "Monitor current weather conditions and "
    "hourly weather patterns for Kathmandu."
)

st.divider()


# ==================================================
# CURRENT WEATHER
# ==================================================

st.subheader("🌤️ Current Weather Conditions")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Temperature",
        f"{current['temperature_2m']:.1f} °C"
    )


with col2:

    st.metric(
        "Humidity",
        f"{current['relative_humidity_2m']:.1f}%"
    )


with col3:

    st.metric(
        "Feels Like",
        f"{current['apparent_temperature']:.1f} °C"
    )


with col4:

    st.metric(
        "Rainfall",
        f"{current['precipitation']:.1f} mm"
    )


# ==================================================
# WIND
# ==================================================

st.subheader("💨 Wind Conditions")

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']:.1f} km/h"
    )


with col2:

    st.metric(
        "Wind Direction",
        f"{current['wind_direction_10m']:.0f}°"
    )


st.divider()


# ==================================================
# TEMPERATURE TREND
# ==================================================

st.subheader("🌡️ Temperature Trend")

fig_temp = px.line(
    hourly_df,
    x="time",
    y="temperature_2m",
    title="Hourly Temperature",
    labels={
        "time": "Time",
        "temperature_2m": "Temperature (°C)"
    }
)

st.plotly_chart(
    fig_temp,
    use_container_width=True
)


# ==================================================
# HUMIDITY TREND
# ==================================================

st.subheader("💧 Humidity Trend")

fig_humidity = px.line(
    hourly_df,
    x="time",
    y="relative_humidity_2m",
    title="Hourly Relative Humidity",
    labels={
        "time": "Time",
        "relative_humidity_2m":
            "Relative Humidity (%)"
    }
)

st.plotly_chart(
    fig_humidity,
    use_container_width=True
)


# ==================================================
# RAINFALL
# ==================================================

st.subheader("🌧️ Precipitation")

fig_rain = px.bar(
    hourly_df,
    x="time",
    y="precipitation",
    title="Hourly Precipitation",
    labels={
        "time": "Time",
        "precipitation": "Precipitation (mm)"
    }
)

st.plotly_chart(
    fig_rain,
    use_container_width=True
)


# ==================================================
# WIND SPEED
# ==================================================

st.subheader("💨 Wind Speed Trend")

fig_wind = px.line(
    hourly_df,
    x="time",
    y="wind_speed_10m",
    title="Hourly Wind Speed",
    labels={
        "time": "Time",
        "wind_speed_10m": "Wind Speed (km/h)"
    }
)

st.plotly_chart(
    fig_wind,
    use_container_width=True
)


# ==================================================
# WEATHER DATA TABLE
# ==================================================

st.subheader("📋 Hourly Weather Data")

st.dataframe(
    hourly_df,
    use_container_width=True,
    hide_index=True
)