import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Explorer | Climate Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(content)


# ============================================================
# SAME OVERVIEW UI / CSS
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
    max-width: 920px;
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

.info-card {
    min-height: 120px;
    padding: 21px;
    border-radius: 18px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 30px rgba(0,0,0,0.16);
}

.info-label {
    color: #7890a5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 9px;
}

.info-value {
    color: #f3f8fd;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 6px;
}

.info-detail {
    color: #8297aa;
    font-size: 13px;
    line-height: 1.5;
}

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 11px;
}

div[data-testid="stDateInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
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

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    overflow: hidden;
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

    if "time" in df.columns:
        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )
        df = df.dropna(subset=["time"])
        df = df.sort_values("time")

    return df.reset_index(drop=True)


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

    st.markdown("### 📊 Data Explorer")

    st.caption(
        "Search, filter, inspect, and download climate observations."
    )

    st.markdown("---")

    if "time" in climate_df.columns:

        min_date = climate_df["time"].min().date()
        max_date = climate_df["time"].max().date()

        st.markdown("### 📅 Date Range")

        date_columns = st.columns(2)

        with date_columns[0]:
            start_date = st.date_input(
                "From",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="explorer_start"
            )

        with date_columns[1]:
            end_date = st.date_input(
                "To",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="explorer_end"
            )

    st.markdown("### 🔎 Search")

    search_text = st.text_input(
        "Search data",
        placeholder="Search values...",
        label_visibility="collapsed"
    )

    st.markdown("### 📈 Numeric Metric")

    numeric_columns = climate_df.select_dtypes(
        include="number"
    ).columns.tolist()

    metric_options = ["None"] + numeric_columns

    selected_metric = st.selectbox(
        "Metric",
        metric_options,
        label_visibility="collapsed"
    )

    st.markdown("### 🔢 Rows to Display")

    max_rows = st.number_input(
        "Rows",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
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
        <b>DATA EXPLORER</b><br>
        🔎 Search observations<br>
        📅 Filter by date<br>
        📊 Inspect metrics<br>
        ⬇️ Export filtered data
    </div>
    """)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = climate_df.copy()

if "time" in filtered_df.columns:

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    start_timestamp = pd.Timestamp(start_date)

    end_timestamp = (
        pd.Timestamp(end_date) +
        pd.Timedelta(days=1)
    )

    filtered_df = filtered_df[
        (filtered_df["time"] >= start_timestamp) &
        (filtered_df["time"] < end_timestamp)
    ]


# ============================================================
# SEARCH ALL COLUMNS
# ============================================================

if search_text.strip():

    search_mask = filtered_df.astype(
        str
    ).apply(
        lambda column: column.str.contains(
            search_text,
            case=False,
            na=False
        )
    ).any(axis=1)

    filtered_df = filtered_df[search_mask]


# ============================================================
# HERO
# ============================================================

html("""
<div class="hero">

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="live-badge">
            ● DATA EXPLORATION CENTER
        </div>

        <div class="hero-title">
            Climate Data Explorer
        </div>

        <div class="hero-subtitle">
            Explore climate observations interactively.
            Filter the dataset, inspect individual variables,
            identify patterns, and export the selected records
            for further analysis.
        </div>

    </div>

</div>
""")


# ============================================================
# DATASET KPIs
# ============================================================

st.markdown("### 📊 Dataset Overview")
st.caption(
    "A quick view of the currently filtered climate dataset."
)

total_records = len(filtered_df)
total_columns = len(filtered_df.columns)

missing_values = int(
    filtered_df.isna().sum().sum()
)

duplicate_rows = int(
    filtered_df.duplicated().sum()
)

kpis = [
    ("📋", "Filtered Records", f"{total_records:,}"),
    ("🧩", "Columns", f"{total_columns}"),
    ("⚠️", "Missing Values", f"{missing_values:,}"),
    ("♻️", "Duplicate Rows", f"{duplicate_rows:,}")
]

kpi_columns = st.columns(4)

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
# FILTERED DATA STATUS
# ============================================================

st.markdown("### 🔎 Active Dataset")

if filtered_df.empty:

    st.warning(
        "No records match the selected filters."
    )

else:

    info_columns = st.columns(3)

    if "time" in filtered_df.columns:
        first_record = filtered_df["time"].min()
        last_record = filtered_df["time"].max()

        info_items = [
            (
                "FIRST OBSERVATION",
                first_record.strftime("%Y-%m-%d %H:%M"),
                "Earliest record currently displayed."
            ),
            (
                "LATEST OBSERVATION",
                last_record.strftime("%Y-%m-%d %H:%M"),
                "Latest record currently displayed."
            ),
            (
                "FILTERED ROWS",
                f"{len(filtered_df):,}",
                "Records remaining after filters."
            )
        ]

    else:

        info_items = [
            (
                "DATASET",
                "Climate Data",
                "Current dataset."
            ),
            (
                "FILTERED ROWS",
                f"{len(filtered_df):,}",
                "Records remaining after filters."
            ),
            (
                "COLUMNS",
                f"{len(filtered_df.columns)}",
                "Variables available."
            )
        ]

    for column, item in zip(info_columns, info_items):

        label, value, detail = item

        with column:
            html(f"""
            <div class="info-card">

                <div class="info-label">
                    {label}
                </div>

                <div class="info-value">
                    {value}
                </div>

                <div class="info-detail">
                    {detail}
                </div>

            </div>
            """)


# ============================================================
# SELECTED METRIC ANALYSIS
# ============================================================

if (
    selected_metric != "None"
    and selected_metric in filtered_df.columns
    and not filtered_df.empty
):

    st.markdown("### 📈 Selected Metric Analysis")

    metric_series = pd.to_numeric(
        filtered_df[selected_metric],
        errors="coerce"
    ).dropna()

    if not metric_series.empty:

        metric_cols = st.columns(4)

        metric_stats = [
            ("AVERAGE", f"{metric_series.mean():.2f}"),
            ("MINIMUM", f"{metric_series.min():.2f}"),
            ("MAXIMUM", f"{metric_series.max():.2f}"),
            ("MEDIAN", f"{metric_series.median():.2f}")
        ]

        for column, item in zip(metric_cols, metric_stats):

            label, value = item

            with column:
                html(f"""
                <div class="info-card">

                    <div class="info-label">
                        {label}
                    </div>

                    <div class="info-value">
                        {value}
                    </div>

                    <div class="info-detail">
                        {selected_metric}
                    </div>

                </div>
                """)

        if "time" in filtered_df.columns:

            chart_df = filtered_df[
                ["time", selected_metric]
            ].copy()

            chart_df[selected_metric] = pd.to_numeric(
                chart_df[selected_metric],
                errors="coerce"
            )

            chart_df = chart_df.dropna()

            if not chart_df.empty:

                fig_metric = px.line(
                    chart_df,
                    x="time",
                    y=selected_metric,
                    labels={
                        "time": "",
                        selected_metric: selected_metric
                    }
                )

                fig_metric.update_layout(
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
                        showgrid=False
                    ),
                    yaxis=dict(
                        gridcolor="rgba(255,255,255,0.07)"
                    ),
                    hovermode="x unified",
                    font=dict(color="#b9c8d8")
                )

                st.plotly_chart(
                    fig_metric,
                    use_container_width=True
                )


# ============================================================
# DATA QUALITY
# ============================================================

st.markdown("### 🧹 Data Quality Overview")

quality_left, quality_right = st.columns(2)

with quality_left:

    missing_df = (
        filtered_df.isna()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ].sort_values(
        "Missing Values",
        ascending=False
    )

    if missing_df.empty:

        html("""
        <div class="info-card">
            <div class="info-label">
                MISSING DATA
            </div>
            <div class="info-value">
                0
            </div>
            <div class="info-detail">
                No missing values were found in the filtered dataset.
            </div>
        </div>
        """)

    else:

        fig_missing = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            labels={
                "Column": "",
                "Missing Values": "Missing Values"
            }
        )

        fig_missing.update_layout(
            height=390,
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
            fig_missing,
            use_container_width=True
        )


with quality_right:

    dtype_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": [
            str(dtype)
            for dtype in filtered_df.dtypes
        ]
    })

    dtype_counts = (
        dtype_df["Data Type"]
        .value_counts()
        .reset_index()
    )

    dtype_counts.columns = [
        "Data Type",
        "Columns"
    ]

    fig_dtype = px.bar(
        dtype_counts,
        x="Data Type",
        y="Columns",
        labels={
            "Data Type": "",
            "Columns": "Number of Columns"
        }
    )

    fig_dtype.update_layout(
        height=390,
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
        fig_dtype,
        use_container_width=True
    )


# ============================================================
# COMPLETE DATA TABLE
# ============================================================

st.markdown("### 📋 Explore Records")

if filtered_df.empty:

    st.info(
        "Try changing the date range or search term."
    )

else:

    display_df = filtered_df.copy()

    if "time" in display_df.columns:
        display_df = display_df.sort_values(
            "time",
            ascending=False
        )

    display_df = display_df.head(
        int(max_rows)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        height=520
    )

    st.caption(
        f"Showing {len(display_df):,} of "
        f"{len(filtered_df):,} filtered records."
    )


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("### ⬇️ Export")

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Filtered Climate Data",
    data=csv_data,
    file_name="filtered_climate_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">

    <b>🌍 Climate Intelligence Dashboard</b>

    <br>

    Interactive Climate Data Explorer

    <br><br>

    Built with Python • Pandas • Plotly • Streamlit

    <br>

    Data prepared for climate and environmental analysis

</div>
""")
