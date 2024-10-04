import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    daily_orders_df = df.groupby('mnth')['cnt_x'].sum()
    
    return daily_orders_df

def create_sum_order_items_df(df):
    usage_comparison = df.groupby('workingday_x').agg({
    'casual_x': 'sum',
    'registered_x': 'sum'
    }).reset_index()

    # Mengubah workingday menjadi label yang lebih informatif
    usage_comparison['workingday_x'] = usage_comparison['workingday_x'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    return usage_comparison

def create_bygender_df(df):
    # Mengelompokkan data berdasarkan weathersit dan workingday
    weather_usage = df.groupby(['weathersit_x', 'workingday_x']).agg({'cnt_x': 'sum'}).reset_index()

# Mengubah workingday menjadi label yang lebih informatif
    weather_usage['workingday_x'] = weather_usage['workingday_x'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    return weather_usage

def create_byage_df(df):
    # Menghitung total penggunaan sepeda dari pengguna terdaftar dan kasual
    total_usage = df[['casual_x', 'registered_x']].sum()
    return total_usage


# Load cleaned data
all_df = pd.read_csv("main.csv")




# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(all_df)
sum_order_items_df = create_sum_order_items_df(all_df)
bygender_df = create_bygender_df(all_df)
byage_df = create_byage_df(all_df)


# plot number of daily orders (2021)
st.header('Bike Data Set')
st.subheader('Annisa Auliya Ramadhani ML-08')



# Product performance
st.subheader("1. Tren Penggunaan Sepeda Sepanjang Bulan Selama Satu Tahun Terakhir")

fig, ax = plt.subplots(figsize=(10, 6))  # Ganti plt.figure() dengan plt.subplots()
daily_orders_df.plot(kind='line', marker='o', ax=ax)  # Menentukan ax di sini
plt.title('Tren Penggunaan Sepeda Sepanjang Bulan Selama Satu Tahun Terakhir')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penggunaan Sepeda')
plt.grid()
plt.xticks(daily_orders_df.index, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])


st.pyplot(fig)

# customer demographic
st.subheader("2. Perbandingan Penggunaan Sepeda antara Pengguna Terdaftar dan Kasual")

# Visualisasi menggunakan stacked bar chart
fig, ax = plt.subplots(figsize=(10, 6))  
plt.bar(sum_order_items_df['workingday_x'], sum_order_items_df['casual_x'], label='Pengguna Kasual', color='lightblue')
plt.bar(sum_order_items_df['workingday_x'], sum_order_items_df['registered_x'], bottom=sum_order_items_df['casual_x'], label='Pengguna Terdaftar', color='orange')

plt.title('Perbandingan Penggunaan Sepeda antara Pengguna Terdaftar dan Kasual')
plt.xlabel('Tipe Hari')
plt.ylabel('Total Penggunaan Sepeda')
plt.legend()
plt.grid(axis='y')
st.pyplot(fig)


# Best Customer Based on RFM Parameters
st.subheader("3. Pengaruh Kondisi Cuaca terhadap Jumlah Penggunaan Sepeda")

fig, ax = plt.subplots(figsize=(10, 6))  
for workingday in bygender_df['workingday_x'].unique():
    subset = bygender_df[bygender_df['workingday_x'] == workingday]
    plt.bar(subset['weathersit_x'], subset['cnt_x'], label=workingday)

plt.title('Pengaruh Kondisi Cuaca terhadap Jumlah Penggunaan Sepeda')
plt.xlabel('Kondisi Cuaca (Weathersit)')
plt.ylabel('Total Penggunaan Sepeda')
plt.xticks(rotation=45)
plt.legend(title='Tipe Hari')
plt.grid(axis='y')
st.pyplot(fig)

st.subheader("4. Kontribusi Pengguna Terdaftar vs Kasual terhadap Total Penggunaan Sepeda")

labels = ['Pengguna Kasual', 'Pengguna Terdaftar']
sizes = byage_df.values
colors = ['lightcoral', 'lightskyblue']
explode = (0.1, 0)  # hanya memisahkan segmen pertama

fig, ax = plt.subplots(figsize=(10, 6))  
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
plt.title('Kontribusi Pengguna Terdaftar vs Kasual terhadap Total Penggunaan Sepeda')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
st.pyplot(fig)