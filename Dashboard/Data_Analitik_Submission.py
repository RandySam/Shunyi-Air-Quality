<<<<<<< HEAD
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("Data/PRSA_Data_Shunyi_20130301-20170228.csv")
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df['month'] = df['datetime'].dt.month
    df['year'] = df['datetime'].dt.year
    return df

df = load_data()

# Filter tahun interaktif untuk pertanyaan 1
st.title("Dashboard Analisis PM2.5 di Distrik Shunyi Tahun 2013–2017")

st.sidebar.header("Navigasi")

menu = st.sidebar.radio("Pilih Visualisasi: ", [
    "Distribusi PM2.5 thaun 2013–2017",
    "Korelasi PM2.5 dengan cuaca"
])

if menu == "Distribusi PM2.5 thaun 2013–2017":
    st.header("1. Tren Musiman PM2.5")
    year_range = st.slider("Pilih rentang tahun", min_value=2013, max_value=2017, value=(2013, 2017))
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    monthly_trend = filtered_df.groupby(['year', 'month'])['PM2.5'].mean().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_trend, x='month', y='PM2.5', hue='year', marker='o', palette='viridis')
    plt.title('Tren Musiman PM2.5 ({}–{})'.format(year_range[0], year_range[1]))
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(ticks=range(1,13), labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
                ### Kesimpulan
                Selama periode 2013 hingga 2017, tingkat konsentrasi PM2.5 di distrik Shunyi menunjukkan pola musiman yang konsisten setiap tahunnya. 
                Nilai PM2.5 cenderung meningkat signifikan selama musim dingin (Desember hingga Februari), 
                dan menurun selama musim panas (Juni hingga Agustus). Hal ini kemungkinan disebabkan oleh 
                peningkatan penggunaan bahan bakar untuk pemanas serta kondisi atmosfer yang kurang mendukung dispersi 
                polutan saat musim dingin. Secara umum, tren tahunan menunjukkan kecenderungan penurunan tingkat polusi, 
                terutama setelah tahun 2014 yang tercatat sebagai tahun dengan tingkat PM2.5 paling tinggi hampir di seluruh bulan. 
                Tren ini dapat mencerminkan dampak kebijakan pengendalian polusi udara 
                atau perbaikan dalam infrastruktur lingkungan.""")

elif menu == "Korelasi PM2.5 dengan cuaca":

    st.header("2. Korelasi PM2.5 dengan Parameter Cuaca (Heatmap)")
    st.markdown("Visualisasi korelasi antara PM2.5 dan variabel cuaca menggunakan heatmap.")

    correlation_matrix = df[["PM2.5", "TEMP", "PRES", "WSPM"]].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Korelasi PM2.5 dengan Cuaca")
    st.pyplot(plt)

    st.markdown("""
                ### Kesimpulan
                Hasil analisis statistik terhadap tiga parameter cuaca — suhu udara (TEMP), tekanan atmosfer (PRES), dan kecepatan angin (WSPM) 
                — menunjukkan bahwa:

                - Kecepatan angin memiliki pengaruh paling signifikan, dengan korelasi 
                negatif sedang terhadap PM2.5. Ini berarti semakin kencang angin, 
                semakin rendah tingkat polusi udara karena partikel polutan tersebar lebih luas.
                - Tekanan udara menunjukkan pengaruh negatif yang sangat lemah namun 
                signifikan secara statistik, menandakan bahwa tekanan tinggi sedikit 
                berkaitan dengan penurunan polusi.
                - Suhu udara tidak memiliki korelasi yang signifikan terhadap PM2.5, 
                sehingga tidak menjadi faktor utama dalam dinamika polusi udara di wilayah ini.""")
=======
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import os

# === Use relative path for dataset ===
DATA_URL = "Data/PRSA_Data_Shunyi_20130301-20170228.csv"

# Check if file exists
if not os.path.exists(DATA_URL):
    # Print current working directory to debug
    st.error(f"Dataset not found at {DATA_URL}")
    st.write(f"Current working directory: {os.getcwd()}")
    # Try alternative path
    # alt_path = "Data/PRSA_Data_Shunyi_20130301-20170228.csv"
    # if os.path.exists(alt_path):
    #     DATA_URL = alt_path
    #     st.success(f"Found dataset at alternative path: {alt_path}")
    # else:
    #     st.stop()
        
DATA_URL = DATA_URL

# === Load Data Function ===
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df.replace("NA", np.nan, inplace=True)
    df = df.apply(pd.to_numeric, errors='ignore')

    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)

    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofweek'] = df.index.dayofweek
    df['is_weekend'] = df['dayofweek'] >= 5
    return df

# === Streamlit UI ===
st.set_page_config(page_title="PM2.5 Shunyi Dashboard", layout="wide")
st.title("📊 PM2.5 Analysis Dashboard - Shunyi, Beijing")
st.markdown("""
Explore air quality data (PM2.5) from Shunyi district using interactive analysis tools. 
This dashboard visualizes pollution trends, weather relationships, and category breakdowns.
""")

df = load_data()

# Sidebar
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Select Year(s)", options=sorted(df['year'].unique()), default=sorted(df['year'].unique()))
view_mode = st.sidebar.radio("View Mode", ['Daily Average', 'Hourly Data'])

df_filtered = df[df['year'].isin(years)]

# === PM2.5 Categorization ===
def categorize_pm25(val):
    if pd.isna(val): return np.nan
    if val <= 50:
        return "Good"
    elif val <= 100:
        return "Moderate"
    elif val <= 150:
        return "Unhealthy for Sensitive"
    elif val <= 200:
        return "Unhealthy"
    elif val <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

df_filtered['PM2.5_category'] = df_filtered['PM2.5'].apply(categorize_pm25)
df_daily = df_filtered.resample('D')[df_filtered.select_dtypes(include='number').columns].mean().copy()
df_daily['PM2.5_category'] = df_daily['PM2.5'].apply(categorize_pm25)

# === Tabs ===
tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "📊 Category Distribution", "🌍 Geospatial"])

# === Tab 1: Trend ===
with tab1:
    st.subheader("Trend Over Time")
    if view_mode == 'Daily Average':
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(data=df_daily, x=df_daily.index, y='PM2.5', ax=ax)
        ax.set_title("Daily Average PM2.5")
        ax.set_ylabel("µg/m³")
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(data=df_filtered, x=df_filtered.index, y='PM2.5', alpha=0.3, linewidth=0.7)
        ax.set_title("Hourly PM2.5")
        ax.set_ylabel("µg/m³")
        st.pyplot(fig)

    st.markdown("### Weather Correlation")
    if 'TEMP' in df.columns and 'WSPM' in df.columns:
        corr = df_filtered[['PM2.5', 'TEMP', 'WSPM']].corr()
        st.dataframe(corr.style.background_gradient(cmap='RdBu_r', axis=1))

# === Tab 2: Redesigned ===
with tab2:
    st.subheader("PM2.5 Quality Categories")

    # Bar chart with counts
    cat_counts = df_daily['PM2.5_category'].value_counts().reindex([
        "Good", "Moderate", "Unhealthy for Sensitive", "Unhealthy", "Very Unhealthy", "Hazardous"], fill_value=0)

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    cat_counts.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax1)
    ax1.set_title("Daily PM2.5 Category Counts")
    ax1.set_xlabel("PM2.5 Category")
    ax1.set_ylabel("Days")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    for i, v in enumerate(cat_counts):
        ax1.text(i, v + 1, str(v), ha='center')
    st.pyplot(fig1)

    # Stacked bar: hourly breakdown
    st.markdown("### Hourly Distribution by PM2.5 Category (%)")
    hourly_dist = df_filtered.groupby(['hour', 'PM2.5_category']).size().unstack(fill_value=0)
    hourly_dist_percent = hourly_dist.div(hourly_dist.sum(axis=1), axis=0) * 100

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    hourly_dist_percent.plot(kind='bar', stacked=True, ax=ax2, colormap='tab20c', width=0.8)
    ax2.set_title("Hourly PM2.5 Category Proportion")
    ax2.set_ylabel("Percentage (%)")
    ax2.set_xlabel("Hour of Day")
    ax2.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# === Tab 3: Geospatial ===
with tab3:
    st.subheader("Geospatial PM2.5 Distribution")
    shunyi_lat, shunyi_lon = 40.125, 116.656
    np.random.seed(42)
    df_daily['lat'] = shunyi_lat + np.random.uniform(-0.01, 0.01, len(df_daily))
    df_daily['lon'] = shunyi_lon + np.random.uniform(-0.01, 0.01, len(df_daily))
    gdf = gpd.GeoDataFrame(df_daily, geometry=[Point(xy) for xy in zip(df_daily['lon'], df_daily['lat'])])

    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(column='PM2.5_category', ax=ax, legend=True, markersize=30, alpha=0.6)
    ax.set_title("Daily PM2.5 Categories (Approx. Location)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    st.pyplot(fig)

st.markdown("---")
st.caption("Data is based on hourly air quality recordings from Shunyi Station (2013–2017). Categories follow AQI PM2.5 standards.")
>>>>>>> da81caeb8357d6d88e0c2efa809e178f1480a5f3
