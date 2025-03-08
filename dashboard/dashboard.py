import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Air Quality Data Analysis")
st.caption("© HarHamz 2025")

@st.cache_data
def load_data():
    df_aotizhongxin = pd.read_csv("data/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
    df_changping = pd.read_csv("data/PRSA_Data_Changping_20130301-20170228.csv")
    df_dingling = pd.read_csv("data/PRSA_Data_Dingling_20130301-20170228.csv")
    df_dongsi = pd.read_csv("data/PRSA_Data_Dongsi_20130301-20170228.csv")
    df_guanyuan = pd.read_csv("data/PRSA_Data_Guanyuan_20130301-20170228.csv")
    df_gucheng = pd.read_csv("data/PRSA_Data_Gucheng_20130301-20170228.csv")
    df_huairou = pd.read_csv("data/PRSA_Data_Huairou_20130301-20170228.csv")
    df_nongzhanguan = pd.read_csv("data/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
    df_shunyi = pd.read_csv("data/PRSA_Data_Shunyi_20130301-20170228.csv")
    df_tiantan = pd.read_csv("data/PRSA_Data_Tiantan_20130301-20170228.csv")
    df_wanliu = pd.read_csv("data/PRSA_Data_Wanliu_20130301-20170228.csv")
    df_wanshouxigong = pd.read_csv("data/PRSA_Data_Wanshouxigong_20130301-20170228.csv")

    df_all = pd.concat([
        df_aotizhongxin, df_changping, df_dingling, df_dongsi, df_guanyuan,
        df_gucheng, df_huairou, df_nongzhanguan, df_shunyi, df_tiantan,
        df_wanliu, df_wanshouxigong
    ], ignore_index=True)

    df_all = df_all.dropna()

    return df_all

df_all = load_data()

st.sidebar.header("User Input")
year = st.sidebar.selectbox("Select Year", [2013, 2014, 2015, 2016, 2017], index=3)  # Default to 2016
station = st.sidebar.selectbox("Select Station", df_all["station"].unique())

df_filtered = df_all[(df_all["year"] == year) & (df_all["station"] == station)]

st.header("1. Highest and Lowest Temperatures by Station")
min_temp = df_all.loc[df_all.groupby("station")["TEMP"].idxmin(), ["station", "TEMP"]].rename(columns={"TEMP": "Min Temp"})
max_temp = df_all.loc[df_all.groupby("station")["TEMP"].idxmax(), ["station", "TEMP"]].rename(columns={"TEMP": "Max Temp"})
df_extremes = min_temp.merge(max_temp, on="station")

fig, ax = plt.subplots(figsize=(8, 5))
stations = df_extremes["station"]
x = np.arange(len(stations))
width = 0.4

ax.bar(x - width/2, df_extremes["Min Temp"], width, label="Min Temp", color="blue", alpha=0.7)
ax.bar(x + width/2, df_extremes["Max Temp"], width, label="Max Temp", color="red", alpha=0.7)

ax.set_xlabel("Station")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Maximum and Minimum Temperatures by Station")
ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45, ha="right")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

for bar in ax.patches:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f"{height:.1f}", ha="center", va="bottom" if height > 0 else "top", fontsize=10)

st.pyplot(fig)

st.header(f"2. Monthly Temperature Trends in {year}")
df_average_temp_year = df_all[df_all["year"] == year].groupby(["station", "month"], as_index=False)["TEMP"].mean().rename(columns={"TEMP": "Average Temp"})

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_average_temp_year, x="month", y="Average Temp", hue="station", markers=True, dashes=False)
plt.title(f"Monthly Average Temperature by Station in {year}")
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1))
plt.grid(True)
plt.xticks(ticks=range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
st.pyplot(plt)

st.header(f"3. Monthly Pollutant Trends in {year}")
df_average_part_year = df_all[df_all["year"] == year].groupby(["station", "month"], as_index=False)[["SO2", "NO2", "CO", "O3"]].mean()

pollutants = ["SO2", "NO2", "CO", "O3"]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"Monthly Average Pollutant Concentrations by Station in {year}", fontsize=16)
axes = axes.flatten()

for i, pollutant in enumerate(pollutants):
    sns.lineplot(data=df_average_part_year, x="month", y=pollutant, hue="station", ax=axes[i], markers=True, dashes=False)
    axes[i].set_title(f"{pollutant} Concentration")
    axes[i].set_xlabel("Month")
    axes[i].set_ylabel(f"{pollutant} Concentration (µg/m³)")
    axes[i].set_xticks(ticks=range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
    axes[i].grid(True)
    axes[i].legend(loc="upper right", bbox_to_anchor=(1.2, 1))

plt.tight_layout()
st.pyplot(fig)

st.header(f"4. Correlation Between Pollutants and Temperature in {year} at {station}")
df_station_year = df_all[(df_all["year"] == year) & (df_all["station"] == station)]
df_station_year_avg = df_station_year.groupby("month", as_index=False)[["SO2", "NO2", "CO", "O3", "TEMP"]].mean()

plt.figure(figsize=(8, 6))
sns.heatmap(df_station_year_avg[["SO2", "NO2", "CO", "O3", "TEMP"]].corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
plt.title(f"Pollutants to Temperature Correlation Heatmap in {year} at {station}")
st.pyplot(plt)

st.header("Conclusion")
st.write("""
- **Q1:** The highest temperature recorded was in Gucheng at 41.6 °C, and the lowest was in Huairou at -19.9 °C.
- **Q2:** In 2016, all stations experienced their lowest temperatures in January and highest in July - August.
- **Q3:** SO₂, NO₂, and CO concentrations peak in winter months, while O₃ peaks in summer.
- **Q4:** There is a strong positive correlation between SO₂, NO₂, and CO, and a strong negative correlation between O₃ and temperature.
""")