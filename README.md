# 🚀 Air Quality EDA Dashboard

A **Streamlit** web app for **Exploratory Data Analysis (EDA)** on Air Quality data (PRSA Dataset - Shunyi District).

---

## 📂 Project Overview

Dashboard ini dirancang untuk melakukan analisis eksploratif terhadap data kualitas udara di distrik Shunyi, Beijing. Beberapa fitur utama:

- Visualisasi tren PM2.5 secara interaktif
- Kategori kualitas udara harian dan per jam
- Korelasi antara cuaca dan polusi (TEMP, WSPM, dll)
- Visualisasi geospasial (lokasi acak di sekitar Shunyi)
- Upload dataset langsung melalui UI Streamlit

---

## 📊 Dataset

Aplikasi ini menggunakan dataset **PRSA Data Shunyi**, yang berisi data polusi udara dan parameter cuaca:

- **Periode:** 1 Maret 2013 – 28 Februari 2017
- **Fitur:** `PM2.5`, `PM10`, `SO2`, `NO2`, `CO`, `O3`, `TEMP`, `PRES`, `WSPM`, dan lainnya.

> 🗂️ File yang dibutuhkan: `PRSA_Data_Shunyi_20130301-20170228.csv`  
> File dapat di-upload melalui sidebar ketika aplikasi berjalan.

---

## ⚙️ Cara Menjalankan Proyek

Pastikan kamu sudah memiliki **Python 3.8+**.

Untuk menjalankan proyek ini:

```bash
# (Opsional) Buat virtual environment
python -m venv venv
# Aktifkan (Windows)
venv\Scripts\activate
# atau Aktifkan (Mac/Linux)
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt

# Jalankan Streamlit app
streamlit run Data_Analitik_Submission.py
