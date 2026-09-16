import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Climate Impact",
    page_icon="🌍",
    layout="wide"
)


# ==================================================
# LOCATION
# ==================================================

latitude = 27.7172
longitude = 85.3240


# ==================================================
# GET CLIMATE DATA
# ==================================================

def get_climate_data():

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

        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
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

    air_response = requests.get(
        air_url,
        params=air_params,
        timeout=30
    )

    air_response.raise_for_status()

    air_data = air_response.json()


    # ----------------------------------------------
    # COMBINE DATA
    # ----------------------------------------------

    weather_df = pd.DataFrame(
        weather_data["hourly"]
    )

    air_df = pd.DataFrame(
        air_data["hourly"]
    )

    weather_df["time"] = pd.to_datetime(
        weather_df["time"]
    )

    air_df["time"] = pd.to_datetime(
        air_df["time"]
    )


    climate_df = pd.merge(
        weather_df,
        air_df,
        on="time",
        how="inner"
    )

    return climate_df


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
# LOAD DATA
# ==================================================

try:

    climate_df = get_climate_data()

except Exception as e:

    st.error(
        f"Unable to collect climate data: {e}"
    )

    st.stop()


# ==================================================
# APPLY INDICATORS
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

st.title("🌍 Climate Impact Analysis")

st.write(
    "Analyze temperature, rainfall, air pollution, "
    "and environmental impact indicators for Kathmandu."
)

st.divider()


# ==================================================
# SUMMARY
# ==================================================

st.subheader("📊 Climate Impact Summary")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Average Temperature",
        f"{climate_df['temperature_2m'].mean():.1f} °C"
    )


with col2:

    st.metric(
        "Maximum Temperature",
        f"{climate_df['temperature_2m'].max():.1f} °C"
    )


with col3:

    st.metric(
        "Total Precipitation",
        f"{climate_df['precipitation'].sum():.1f} mm"
    )


with col4:

    st.metric(
        "Maximum AQI",
        f"{climate_df['european_aqi'].max():.0f}"
    )


st.divider()


# ==================================================
# CLIMATE INDICATORS
# ==================================================

st.subheader("🌍 Climate Impact Indicators")

latest = climate_df.iloc[-1]


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
        "🌫️ Air Pollution Indicator",
        latest["air_pollution_indicator"]
    )


# ==================================================
# ENVIRONMENTAL STATUS
# ==================================================

st.subheader("🌍 Environmental Status")

status = latest["environmental_status"]

if status == "High Environmental Impact":

    st.error(
        f"Current Status: **{status}**"
    )

elif status == "Moderate Environmental Impact":

    st.warning(
        f"Current Status: **{status}**"
    )

else:

    st.success(
        f"Current Status: **{status}**"
    )


st.divider()


# ==================================================
# TEMPERATURE ANALYSIS
# ==================================================

st.subheader("🔥 Temperature Impact")

fig_temp = px.line(
    climate_df,
    x="time",
    y="temperature_2m",
    title="Temperature Over Time",
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
# RAINFALL ANALYSIS
# ==================================================

st.subheader("🌧️ Rainfall Impact")

fig_rain = px.bar(
    climate_df,
    x="time",
    y="precipitation",
    title="Precipitation Over Time",
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
# AIR POLLUTION ANALYSIS
# ==================================================

st.subheader("🌫️ Air Pollution Impact")

fig_pollution = px.line(
    climate_df,
    x="time",
    y="european_aqi",
    title="European AQI Over Time",
    labels={
        "time": "Time",
        "european_aqi": "European AQI"
    }
)

st.plotly_chart(
    fig_pollution,
    use_container_width=True
)


# ==================================================
# INDICATOR DISTRIBUTION
# ==================================================

st.subheader("📊 Environmental Indicator Distribution")

indicator_counts = pd.DataFrame({

    "Indicator": [
        "Heat",
        "Rainfall",
        "Air Pollution"
    ],

    "Current Status": [
        latest["heat_indicator"],
        latest["rainfall_indicator"],
        latest["air_pollution_indicator"]
    ]
})


st.dataframe(
    indicator_counts,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# CLIMATE DATA TABLE
# ==================================================

st.subheader("📋 Climate Impact Data")

st.dataframe(
    climate_df,
    use_container_width=True,
    hide_index=True
)