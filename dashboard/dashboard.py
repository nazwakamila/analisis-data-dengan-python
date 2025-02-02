import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style('dark')

def create_daily_recap(df):
    daily_recap = df.groupby(by='dteday').agg({
        'count_cr': 'sum'
    }).reset_index()
    return daily_recap

def count_by_day(day):
    day_count_2011 = day.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_count_2011

def total_registered(day):
   reg =  day.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg = reg.reset_index()
   reg.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg

def total_casual(day):
   cas =  day.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas = cas.reset_index()
   cas.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas

def sum_order (hour):
    sum_order_items_ = hour.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_

def macem_season (day): 
    season_ = day.groupby(by="season").count_cr.sum().reset_index() 
    return season_

# Membaca file CSV
main_data_day = pd.read_csv("dashboard/main_data_day.csv")
main_data_hour = pd.read_csv("dashboard/main_data_hour.csv")

datetime_columns = ["dteday"]
main_data_day.sort_values(by="dteday", inplace=True)
main_data_day.reset_index(inplace=True)   

main_data_hour.sort_values(by="dteday", inplace=True)
main_data_hour.reset_index(inplace=True)

for column in datetime_columns:
    main_data_day[column] = pd.to_datetime(main_data_day[column])
    main_data_hour[column] = pd.to_datetime(main_data_hour[column])

min_date_days = main_data_day["dteday"].min()
max_date_days = main_data_day["dteday"].max()

min_date_hour = main_data_hour["dteday"].min()
max_date_hour = main_data_hour["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/foto_sepeda.png")
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_days = main_data_day[(main_data_day["dteday"] >= str(start_date)) & 
                       (main_data_day["dteday"] <= str(end_date))]

main_hour = main_data_hour[(main_data_hour["dteday"] >= str(start_date)) & 
                        (main_data_hour["dteday"] <= str(end_date))]

daily_recap_df = create_daily_recap(main_hour)
day_count_2011 = count_by_day(main_days)
reg = total_registered(main_days)
cas = total_casual(main_days)
sum_order_items = sum_order(main_hour)
season = macem_season(main_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.title('Bike Sharing :bar_chart:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    daily_recap = daily_recap_df['count_cr'].sum()
    st.metric('Total User', value= daily_recap)

with col2:
    total_sum = reg.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)
    
st.subheader("Visualisasi Bar Chart Antar-Musim")
grouped_day = pd.DataFrame({
    "count_cr": [0.471348, 0.841613, 0.918589, 1.061129],
}, index=["Musim Dingin", "Musim Panas", "Musim Semi", "Musim Gugur"])

# Sorting by values
grouped_day = grouped_day.sort_values(by="count_cr", ascending=False)

# Define color palette
colors = sns.color_palette(["#FF7043", "#FFEB3B", "#80D6FF", "#66BB6A"], n_colors=len(grouped_day))

# Create figure
fig, ax = plt.subplots(figsize=(15, 6))  

# Plot bar chart
sns.barplot(
    y=grouped_day.index,   
    x=grouped_day["count_cr"],  
    palette=colors,  
    ax=ax, 
    order=grouped_day.index  
)

# Set titles and labels
ax.set_title("Bar Chart Antar-Musim", loc="center", fontsize=22)
ax.set_ylabel('Season', fontsize=20)
ax.set_xlabel('Count_cr', fontsize=20)

# Customize tick label size
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)

# Display plot
st.pyplot(fig)

st.subheader('Data Count_cr per Musim')
st.write(grouped_day)

st.subheader("Penggunaan Sepeda Berdasarkan Waktu Terbanyak dan Tersedikit")
# Menghitung jumlah penyewaan sepeda per jam
hour_count = sum_order_items.groupby('hours')['count_cr'].sum().reset_index()

# Mengurutkan berdasarkan penyewa terbanyak dan sedikit
top_rentals = hour_count.sort_values(by="count_cr", ascending=False).head(5)
least_rentals = hour_count.sort_values(by="count_cr", ascending=True).head(5)

# Mengatur warna untuk top dan least rentals
top_colors = ["#D3D3D3", "#D3D3D3", "#074799", "#D3D3D3", "#D3D3D3"]
least_colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#F26B0F", "#D3D3D3"]

# Membuat plot dengan dua sub-plot
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 15))

# Plot untuk jam dengan penyewa terbanyak
sns.barplot(
    x="hours",
    y="count_cr",
    data=top_rentals,
    hue="hours",
    palette=top_colors,
    ax=ax[0]
)
ax[0].set_ylabel("Jumlah Penyewaan Sepeda", fontsize=30)
ax[0].set_xlabel("Jam Malam (PM)", fontsize=30)
ax[0].set_title("Jam dengan Penyewa Sepeda Terbanyak", loc="center", fontsize=30)
ax[0].tick_params(axis='x', labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].legend(title="Hour", title_fontsize=20, fontsize=15)

# Plot untuk jam dengan penyewa paling sedikit
sns.barplot(
    x="hours",
    y="count_cr",
    data=least_rentals,
    hue="hours",
    palette=least_colors,
    ax=ax[1]
)
ax[1].set_ylabel("Jumlah Penyewaan Sepeda", fontsize=30)
ax[1].set_xlabel("Jam Pagi (AM)", fontsize=30)
ax[1].set_title("Jam dengan Penyewa Sepeda Tersedikit", loc="center", fontsize=30)
ax[1].invert_xaxis()  
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].legend(title="Hour", title_fontsize=20, fontsize=15)

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Menampilkan tabel hour_count di bawah grafik
st.subheader('Data Penyewaan Sepeda per Jam')
st.write(hour_count) 

st.subheader("Perbandingan Jumlah Pengguna Casual vs Pengguna Teregistrasi")
# Data untuk bar chart
total_casual = 620017
total_registered = 2672662

# Data untuk bar chart
data = [total_casual, total_registered]
labels = ['Casual', 'Registered']
colors = ["#F26B0F", "#074799"]

# Membuat bar chart
fig, ax = plt.subplots()
ax.bar(labels, data, color=colors)

# Menambahkan label dan judul
ax.set_xlabel('Tipe Pengguna', fontsize=14)
ax.set_ylabel('Total Rental', fontsize=14)
ax.set_title('Total Casual vs Registered Rentals', fontsize=16)

# Streamlit: Menampilkan bar chart
st.pyplot(fig)

# Menampilkan DataFrame yang berisi informasi tentang Total Rentals
st.subheader('Data Total Rentals per Tipe Pengguna')
data_dict = {
    'Tipe Pengguna': ['Casual', 'Registered'],
    'Total Rental': [total_casual, total_registered]
}
total_pengguna_df = pd.DataFrame(data_dict)

# Menampilkan tabel di Streamlit
st.write(total_pengguna_df)

st.subheader("Pola Penyewaan Sepeda Antara Hari Kerja vs Akhir Pekan")

weekday_data = pd.DataFrame({
    'casual': [140521, 70784, 57843, 57319, 61460, 78238, 153852], 
    'registered': [303506, 384719, 411266, 415729, 423935, 409552, 323955]  
}, index=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])

# Membuat plot dengan dua sumbu y
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot pengguna casual pada sumbu y pertama
color = 'tab:blue'
ax1.set_xlabel('Hari dalam Seminggu')
ax1.set_ylabel('Pengguna Casual', color=color)
ax1.plot(weekday_data.index, weekday_data['casual'], color=color, marker='o', label='Casual')
ax1.tick_params(axis='y', labelcolor=color)

# Menambahkan angka di atas titik untuk pengguna casual
for x, y in zip(weekday_data.index, weekday_data['casual']):
    ax1.text(x, y, f'{y:,}', color=color, ha='center', va='bottom', fontsize=10)

# Plot pengguna registered pada sumbu y kedua
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Pengguna Teregistrasi', color=color)
ax2.plot(weekday_data.index, weekday_data['registered'], color=color, marker='o', label='Registered')
ax2.tick_params(axis='y', labelcolor=color)

# Menambahkan angka di atas titik untuk pengguna registered
for x, y in zip(weekday_data.index, weekday_data['registered']):
    ax2.text(x, y, f'{y:,}', color=color, ha='center', va='bottom', fontsize=10)

# Menambahkan judul dan rotasi pada label x-axis
plt.title('Pola Penyewaan Sepeda Antara Hari Kerja vs Akhir Pekan', fontsize=20)
plt.xticks(rotation=45)

# Menyesuaikan layout agar lebih rapi
fig.tight_layout()

# Streamlit: Menampilkan plot
st.pyplot(fig)

# Menampilkan data sebagai tabel di bawah grafik
st.subheader('Data Pengguna Casual vs Registered')
st.write(weekday_data)

st.subheader("Total Peminjaman Setiap Bulannya")

monthly_revenue = pd.Series({
    'Januari': 134933,
    'Febuari': 151352,
    'Maret': 228920,
    'April': 269094,
    'Mei': 331686,
    'Juni': 346342,
    'Juli': 344948,
    'Agustus': 351194,
    'September': 345991,
    'Oktober': 322352,
    'November': 254831,
    'Desember': 211036
})

colors = ['red' if month == 'Agustus' else 'tab:blue' for month in monthly_revenue.index]

plt.figure(figsize=(12, 6))  
bars = plt.bar(monthly_revenue.index, monthly_revenue.values, color=colors)

# Menambahkan legend untuk warna
red_patch = plt.Line2D([0], [0], color='red', lw=4, label='Bulan Sewa Terbanyak (Agustus)')
blue_patch = plt.Line2D([0], [0], color='tab:blue', lw=4, label='Bulan Lainnya')
plt.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize=10)

# Menambahkan judul dan label
plt.title('Total Penyewaan Sepeda per Bulan', fontsize=16, pad=20)
plt.xlabel('Bulan', fontsize=14, labelpad=10)
plt.ylabel('Total Penyewaan', fontsize=14, labelpad=10)
plt.xticks(rotation=45, fontsize=12)  
plt.yticks(fontsize=12)

# Menambahkan nilai di atas setiap bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, height + 5000,  
        f'{int(height)}',  
        ha='center', va='bottom', fontsize=10
    )

# Menyesuaikan layout agar lebih rapi
plt.tight_layout()

# Streamlit: Menampilkan grafik
st.pyplot(plt)

# Menampilkan data sebagai tabel di bawah grafik
st.subheader('Data Penyewaan Sepeda per Bulan')
st.write(monthly_revenue)