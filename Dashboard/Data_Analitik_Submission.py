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