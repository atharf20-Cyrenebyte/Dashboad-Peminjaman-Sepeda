import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_dataHarian():
    df = pd.read_csv("data_harian.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

@st.cache_data
def load_dataJam():
    df = pd.read_csv("data_jam.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df_harian = load_dataHarian()
df_jam = load_dataJam()

# Sidebar untuk filter tanggal
with st.sidebar:
    start_date, end_date = st.date_input("Pilih Rentang Tanggal", 
                                         [df_harian['dteday'].min(), df_harian['dteday'].max()])

# Terapkan filter ke kedua dataset
df_filtered_harian = df_harian[(df_harian['dteday'] >= pd.to_datetime(start_date)) & 
                               (df_harian['dteday'] <= pd.to_datetime(end_date))]

df_filtered_jam = df_jam[(df_jam['dteday'] >= pd.to_datetime(start_date)) & 
                         (df_jam['dteday'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title("📊 Dashboard Peminjaman Sepeda")

# Tambahkan Ringkasan Data
st.metric("Total Peminjaman Sepeda", f"{df_filtered_harian['cnt'].sum():,}")
st.metric("Rata-rata Peminjaman/Hari", f"{df_filtered_harian['cnt'].mean():.2f}")

# Visualisasi: Tren Peminjaman Sepeda
st.subheader(f"Tren Peminjaman Sepeda dari {start_date} hingga {end_date}")
fig, ax = plt.subplots(figsize=(10, 5))
sns.set_style("whitegrid")
sns.lineplot(x=df_filtered_harian['dteday'], y=df_filtered_harian['cnt'], ax=ax, color="blue")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Visualisasi: Pengaruh Cuaca terhadap Peminjaman
st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=df_filtered_harian['weathersit'], y=df_filtered_harian['cnt'], estimator="mean", ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# Visualisasi: Peminjaman Berdasarkan Musim
st.subheader("Perbedaan Peminjaman di Berbagai Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=df_filtered_harian['season'], y=df_filtered_harian['cnt'], estimator="mean", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# Visualisasi: Perbandingan Pengguna Kasual vs Terdaftar
st.subheader("Perbandingan Pengguna Kasual vs Terdaftar")
fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(x=["Casual", "Registered"], y=[df_filtered_jam['casual'].sum(), df_filtered_jam['registered'].sum()], ax=ax)
ax.set_xlabel("Tipe Pengguna")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# Visualisasi: Pola Peminjaman Per Jam
st.subheader("Pola Peminjaman Sepeda Per Jam")
hourly_avg = df_filtered_jam.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker="o", color="blue", linewidth=2, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

st.caption('Copyright © Dicoding 2023')
