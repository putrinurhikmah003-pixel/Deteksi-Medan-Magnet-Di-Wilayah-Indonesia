
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pygeomag import GeoMag
from datetime import date

# ==========================================
# KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="Deteksi Medan Magnet Indonesia",
    page_icon="🧲",
    layout="wide"
)

st.title("🧲 DETEKSI MEDAN MAGNET BUMI")
st.subheader("Visualisasi Persebaran Medan Magnet di Wilayah Indonesia")

st.markdown("""
Aplikasi ini digunakan untuk menghitung dan memvisualisasikan
estimasi medan magnet bumi berdasarkan koordinat geografis
di berbagai wilayah Indonesia menggunakan model WMM-2025.
""")

st.divider()

# ==========================================
# DATA KOTA DI INDONESIA
# ==========================================

data_kota = {
    "Kota": [
        "Banda Aceh", "Medan", "Padang", "Pekanbaru",
        "Palembang", "Bandar Lampung", "Jakarta",
        "Bandung", "Semarang", "Yogyakarta",
        "Surabaya", "Denpasar", "Pontianak",
        "Banjarmasin", "Balikpapan", "Makassar",
        "Manado", "Palu", "Ambon", "Jayapura"
    ],

    "Latitude": [
        5.5483, 3.5952, -0.9471, 0.5071,
        -2.9761, -5.3971, -6.2088,
        -6.9175, -6.9667, -7.7956,
        -7.2575, -8.6500, -0.0263,
        -3.3186, -1.2379, -5.1477,
        1.4748, -0.9003, -3.6954, -2.5337
    ],

    "Longitude": [
        95.3238, 98.6722, 100.3543, 101.4478,
        104.7754, 105.2668, 106.8456,
        107.6191, 110.4167, 110.3695,
        112.7521, 115.2167, 109.3425,
        114.5944, 116.8529, 119.4327,
        124.8420, 119.8707, 128.1814, 140.7181
    ]
}

df_kota = pd.DataFrame(data_kota)

# ==========================================
# INISIALISASI MODEL WMM
# ==========================================

@st.cache_resource
def load_model():
    return GeoMag()

geo_mag = load_model()

# ==========================================
# FUNGSI PERHITUNGAN MEDAN MAGNET
# ==========================================

def hitung_magnet(lat, lon, altitude, tahun):
    hasil = geo_mag.calculate(
        glat=float(lat),
        glon=float(lon),
        alt=float(altitude),
        time=float(tahun)
    )

    return {
        "X - Komponen Utara (nT)": hasil.x,
        "Y - Komponen Timur (nT)": hasil.y,
        "Z - Komponen Vertikal (nT)": hasil.z,
        "H - Medan Horizontal (nT)": hasil.h,
        "F - Intensitas Total (nT)": hasil.f,
        "Deklinasi (derajat)": hasil.d,
        "Inklinasi (derajat)": hasil.i
    }

# ==========================================
# SIDEBAR INPUT
# ==========================================

st.sidebar.header("⚙️ Pengaturan Lokasi")

pilihan_kota = st.sidebar.selectbox(
    "Pilih Kota:",
    df_kota["Kota"]
)

kota_terpilih = df_kota[
    df_kota["Kota"] == pilihan_kota
].iloc[0]

latitude = st.sidebar.number_input(
    "Latitude:",
    min_value=-11.0,
    max_value=6.5,
    value=float(kota_terpilih["Latitude"]),
    format="%.4f"
)

longitude = st.sidebar.number_input(
    "Longitude:",
    min_value=94.0,
    max_value=142.0,
    value=float(kota_terpilih["Longitude"]),
    format="%.4f"
)

altitude = st.sidebar.number_input(
    "Ketinggian (km):",
    min_value=0.0,
    max_value=850.0,
    value=0.0,
    step=0.1
)

tanggal = st.sidebar.date_input(
    "Tanggal analisis:",
    value=date(2026, 11, 18),
    min_value=date(2025, 1, 1),
    max_value=date(2029, 12, 31)
)

# Mengubah tanggal menjadi decimal year
awal_tahun = date(tanggal.year, 1, 1)
akhir_tahun = date(tanggal.year + 1, 1, 1)

tahun_desimal = (
    tanggal.year
    + (tanggal - awal_tahun).days
    / (akhir_tahun - awal_tahun).days
)

# ==========================================
# PERHITUNGAN SELURUH KOTA
# ==========================================

@st.cache_data
def hitung_seluruh_kota(tahun):
    hasil_data = []

    for _, baris in df_kota.iterrows():

        hasil = hitung_magnet(
            baris["Latitude"],
            baris["Longitude"],
            0,
            tahun
        )

        hasil_data.append({
            "Kota": baris["Kota"],
            "Latitude": baris["Latitude"],
            "Longitude": baris["Longitude"],
            **hasil
        })

    return pd.DataFrame(hasil_data)

# ==========================================
# TAMPILAN HASIL UTAMA
# ==========================================

try:

    hasil_lokasi = hitung_magnet(
        latitude,
        longitude,
        altitude,
        tahun_desimal
    )

    st.header("📊 Hasil Analisis Medan Magnet")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Intensitas Total",
        f"{hasil_lokasi['F - Intensitas Total (nT)']:,.2f} nT"
    )

    col2.metric(
        "Medan Horizontal",
        f"{hasil_lokasi['H - Medan Horizontal (nT)']:,.2f} nT"
    )

    col3.metric(
        "Deklinasi",
        f"{hasil_lokasi['Deklinasi (derajat)']:.2f}°"
    )

    st.divider()

    # Tabel komponen medan magnet
    st.subheader("Komponen Medan Magnet")

    tabel_hasil = pd.DataFrame({
        "Parameter": list(hasil_lokasi.keys()),
        "Hasil": [
            round(nilai, 3)
            for nilai in hasil_lokasi.values()
        ]
    })

    st.dataframe(
        tabel_hasil,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # PETA PERSEBARAN INDONESIA
    # ======================================

    st.divider()
    st.header("🗺️ Peta Persebaran Medan Magnet Indonesia")

    df_hasil = hitung_seluruh_kota(tahun_desimal)

    fig = px.scatter_geo(
        df_hasil,
        lat="Latitude",
        lon="Longitude",
        color="F - Intensitas Total (nT)",
        hover_name="Kota",
        hover_data={
            "Latitude": ":.4f",
            "Longitude": ":.4f",
            "F - Intensitas Total (nT)": ":.2f",
            "H - Medan Horizontal (nT)": ":.2f",
            "Latitude": False,
            "Longitude": False
        },
        color_continuous_scale="Turbo",
        projection="mercator",
        title="Estimasi Intensitas Medan Magnet di Indonesia"
    )

    fig.update_geos(
        lonaxis_range=[94, 142],
        lataxis_range=[-12, 8],
        showcountries=True,
        showland=True,
        landcolor="rgb(235,235,235)",
        showocean=True,
        oceancolor="rgb(220,235,250)",
        resolution=50
    )

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(
            title="Intensitas (nT)"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # GRAFIK PERBANDINGAN
    # ======================================

    st.divider()
    st.header("📈 Grafik Perbandingan Intensitas")

    fig_bar = px.bar(
        df_hasil.sort_values(
            "F - Intensitas Total (nT)",
            ascending=False
        ),
        x="Kota",
        y="F - Intensitas Total (nT)",
        color="F - Intensitas Total (nT)",
        color_continuous_scale="Viridis",
        title="Perbandingan Intensitas Medan Magnet Antar Kota"
    )

    fig_bar.update_layout(
        xaxis_title="Kota",
        yaxis_title="Intensitas Total (nT)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # ======================================
    # DATA KESELURUHAN
    # ======================================

    st.divider()
    st.header("📋 Data Hasil Perhitungan")

    st.dataframe(
        df_hasil.round(3),
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # DOWNLOAD CSV
    # ======================================

    csv = df_hasil.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Data CSV",
        data=csv,
        file_name="data_medan_magnet_indonesia.csv",
        mime="text/csv"
    )

    # ======================================
    # INFORMASI ILMIAH
    # ======================================

    st.divider()

    st.subheader("ℹ️ Informasi Aplikasi")

    st.write("""
    - Model: World Magnetic Model 2025 (WMM-2025).
    - Sumber model: NOAA / NCEI.
    - Satuan intensitas: Nanotesla (nT).
    - X: Komponen medan magnet arah utara.
    - Y: Komponen medan magnet arah timur.
    - Z: Komponen medan magnet vertikal.
    - H: Intensitas medan magnet horizontal.
    - F: Intensitas total medan magnet.
    - D: Sudut deklinasi magnetik.
    - I: Sudut inklinasi magnetik.

    Nilai yang ditampilkan merupakan hasil estimasi
    model geomagnetik, bukan pembacaan sensor langsung.
    """)

except Exception as e:
    st.error(f"Terjadi kesalahan perhitungan: {e}")

st.caption(
    "Aplikasi Deteksi Medan Magnet Indonesia | "
    "Python + Streamlit + WMM-2025"
)

# 🧲 Deteksi Medan Magnet Indonesia

## Deskripsi
Aplikasi berbasis Python dan Streamlit untuk
menghitung serta memvisualisasikan estimasi
medan magnet bumi di berbagai wilayah Indonesia.

Aplikasi menggunakan World Magnetic Model 2025
(WMM-2025) melalui library PyGeoMag.

## Fitur
- Perhitungan intensitas medan magnet.
- Analisis komponen X, Y, dan Z.
- Perhitungan medan horizontal dan total.
- Perhitungan deklinasi dan inklinasi.
- Peta persebaran medan magnet Indonesia.
- Grafik perbandingan antar kota.
- Download data hasil perhitungan dalam CSV.

## Teknologi
- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- PyGeoMag
- World Magnetic Model 2025

## Instalasi

Clone repository:

    git clone https://github.com/USERNAME/deteksi-medan-magnet-indonesia.git

Masuk ke folder:

    cd deteksi-medan-magnet-indonesia

Install library:

    pip install -r requirements.txt

Jalankan aplikasi:

    streamlit run app.py

## Sumber Model
NOAA - National Centers for Environmental Information

World Magnetic Model (WMM-2025):
https://www.ncei.noaa.gov/products/world-magnetic-model

## Catatan
Hasil aplikasi merupakan estimasi berdasarkan
model geomagnetik, bukan pengukuran langsung
menggunakan sensor magnetometer.
