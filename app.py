
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pygeomag import GeoMag
from datetime import date

# =====================================================
# 1. KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="Deteksi Medan Magnet Indonesia",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. HEADER APLIKASI
# =====================================================

st.title("🧲 DETEKSI MEDAN MAGNET BUMI")
st.markdown(
    "### Visualisasi dan Analisis Medan Magnet di Wilayah Indonesia"
)

st.markdown("""
Aplikasi ini merupakan media pembelajaran dan analisis
fisika yang digunakan untuk mempelajari medan magnet bumi,
menghitung komponen geomagnetik, serta menampilkan
persebaran estimasi medan magnet di berbagai wilayah Indonesia.
""")

st.divider()

# =====================================================
# 3. NAVIGASI SIDEBAR
# =====================================================

st.sidebar.title("🧭 MENU APLIKASI")

menu = st.sidebar.radio(
    "Pilih Halaman:",
    [
        "Beranda",
        "Materi Medan Magnet",
        "Deteksi Medan Magnet",
        "Peta Persebaran Indonesia",
        "Contoh Soal",
        "Tentang Aplikasi"
    ]
)

# =====================================================
# 4. DATA KOTA INDONESIA
# =====================================================

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

# =====================================================
# 5. MODEL GEOMAGNETIK WMM-2025
# =====================================================

@st.cache_resource
def load_model():
    return GeoMag()

geo_mag = load_model()

# =====================================================
# 6. FUNGSI PERHITUNGAN MEDAN MAGNET
# =====================================================

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

# =====================================================
# 7. FUNGSI PERHITUNGAN SELURUH KOTA
# =====================================================

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

# =====================================================
# 8. HALAMAN BERANDA
# =====================================================

if menu == "Beranda":

    st.header("🌏 Selamat Datang")

    st.write("""
    Selamat datang di aplikasi Deteksi Medan Magnet Bumi
    di Wilayah Indonesia.

    Aplikasi ini dibuat untuk membantu pengguna memahami
    konsep medan magnet bumi melalui penjelasan materi,
    perhitungan komponen medan magnet, grafik, dan peta
    persebaran geomagnetik.
    """)

    st.subheader("🎯 Tujuan Aplikasi")

    st.write("""
    1. Memahami konsep dasar medan magnet bumi.
    2. Mengetahui komponen-komponen medan magnet.
    3. Menghitung estimasi medan magnet berdasarkan koordinat.
    4. Mengamati variasi medan magnet di berbagai wilayah Indonesia.
    5. Menghubungkan konsep fisika dengan kehidupan sehari-hari.
    """)

    st.subheader("🔍 Fitur Utama")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **🧲 Deteksi Medan Magnet**

        Menghitung intensitas medan magnet berdasarkan
        latitude, longitude, ketinggian, dan tanggal.
        """)

        st.info("""
        **📊 Analisis Data**

        Menampilkan komponen X, Y, Z, H, dan F
        dalam satuan nanotesla.
        """)

    with col2:
        st.success("""
        **🗺️ Peta Indonesia**

        Memvisualisasikan persebaran estimasi
        medan magnet di berbagai kota Indonesia.
        """)

        st.success("""
        **📥 Unduh Data**

        Menyediakan hasil perhitungan dalam
        format CSV.
        """)

    st.subheader("⚙️ Teknologi yang Digunakan")

    st.markdown("""
    - **Python:** Bahasa pemrograman utama.
    - **Streamlit:** Membuat aplikasi web interaktif.
    - **Pandas:** Mengolah data hasil perhitungan.
    - **NumPy:** Mendukung komputasi numerik.
    - **Plotly:** Membuat grafik dan visualisasi peta.
    - **PyGeoMag:** Menghitung medan geomagnetik
      berdasarkan model WMM-2025.
    """)

# =====================================================
# 9. HALAMAN MATERI MEDAN MAGNET
# =====================================================

elif menu == "Materi Medan Magnet":

    st.header("📚 MATERI MEDAN MAGNET")

    # PENGERTIAN

    st.subheader("1. Pengertian Medan Magnet")

    st.write("""
    Medan magnet adalah daerah di sekitar magnet,
    kawat berarus listrik, atau benda bermagnet yang
    masih dipengaruhi oleh gaya magnet.

    Medan magnet merupakan besaran vektor yang memiliki
    besar dan arah. Simbol medan magnet adalah B
    dengan satuan SI Tesla (T).

    Bumi juga memiliki medan magnet yang disebut
    medan magnet bumi atau geomagnetik. Medan ini
    sebagian besar dihasilkan oleh pergerakan material
    konduktif di inti luar bumi.
    """)

    st.divider()

    # RUMUS DASAR

    st.subheader("2. Rumus-Rumus Medan Magnet")

    st.markdown("**A. Medan magnet di sekitar kawat lurus panjang**")

    st.latex(r"B = \frac{\mu_0 I}{2\pi r}")

    st.write("""
    Keterangan:
    - B = induksi magnetik (Tesla)
    - μ₀ = permeabilitas vakum (4π × 10⁻⁷ T m/A)
    - I = kuat arus listrik (Ampere)
    - r = jarak dari kawat (meter)
    """)

    st.markdown("**B. Medan magnet di pusat lingkaran berarus**")

    st.latex(r"B = \frac{\mu_0 I}{2R}")

    st.write("""
    Keterangan:
    - R = jari-jari lingkaran (meter)
    - I = kuat arus listrik (Ampere)
    """)

    st.markdown("**C. Gaya magnet pada kawat berarus**")

    st.latex(r"F = B I L \sin\theta")

    st.write("""
    Keterangan:
    - F = gaya magnet (Newton)
    - B = medan magnet (Tesla)
    - I = kuat arus (Ampere)
    - L = panjang kawat (meter)
    - θ = sudut antara arah arus dan medan magnet
    """)

    st.markdown("**D. Hubungan komponen medan magnet bumi**")

    st.latex(r"H = \sqrt{X^2 + Y^2}")

    st.latex(r"F = \sqrt{H^2 + Z^2}")

    st.latex(r"D = \tan^{-1}\left(\frac{Y}{X}\right)")

    st.latex(r"I = \tan^{-1}\left(\frac{Z}{H}\right)")

    st.write("""
    Keterangan:
    - X = komponen medan magnet arah utara (nT)
    - Y = komponen medan magnet arah timur (nT)
    - Z = komponen vertikal (nT)
    - H = intensitas medan horizontal (nT)
    - F = intensitas medan magnet total (nT)
    - D = sudut deklinasi
    - I = sudut inklinasi

    Rumus sudut di atas menggunakan konvensi kuadran
    yang sesuai. Dalam aplikasi, nilai sudut dihitung
    langsung oleh model WMM.
    """)

    st.divider()

    # CONTOH KEHIDUPAN

    st.subheader("3. Contoh Medan Magnet dalam Kehidupan Sehari-hari")

    with st.expander("🧭 1. Kompas"):
        st.write("""
        Jarum kompas dapat menunjukkan arah utara dan selatan
        karena berinteraksi dengan medan magnet bumi.
        """)

    with st.expander("🌍 2. Medan Magnet Bumi"):
        st.write("""
        Medan magnet bumi membantu melindungi lingkungan
        bumi dari sebagian partikel bermuatan yang berasal
        dari matahari dan berperan dalam fenomena aurora.
        """)

    with st.expander("🔊 3. Speaker"):
        st.write("""
        Speaker memanfaatkan interaksi antara medan magnet
        permanen dan arus listrik pada kumparan untuk
        menghasilkan getaran yang kemudian menjadi suara.
        """)

    with st.expander("⚡ 4. Motor Listrik"):
        st.write("""
        Motor listrik menggunakan gaya magnet untuk
        menghasilkan gerakan putar sehingga dapat
        menggerakkan kipas, pompa, dan peralatan lainnya.
        """)

    with st.expander("🧲 5. Magnet pada Pintu Kulkas"):
        st.write("""
        Magnet pada bagian pintu kulkas membantu menjaga
        pintu tetap tertutup dengan menarik bagian logam
        atau material magnetik pada rangka kulkas.
        """)

# =====================================================
# 10. HALAMAN DETEKSI MEDAN MAGNET
# =====================================================

elif menu == "Deteksi Medan Magnet":

    st.header("🧲 DETEKSI MEDAN MAGNET BERDASARKAN LOKASI")

    st.write("""
    Masukkan koordinat geografis untuk mengetahui
    estimasi komponen medan magnet bumi pada lokasi
    yang ingin dianalisis.
    """)

    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Input Koordinat")

    pilihan_kota = st.sidebar.selectbox(
        "Pilih Kota",
        df_kota["Kota"]
    )

    kota = df_kota[
        df_kota["Kota"] == pilihan_kota
    ].iloc[0]

    latitude = st.sidebar.number_input(
        "Latitude",
        min_value=-11.0,
        max_value=6.5,
        value=float(kota["Latitude"]),
        format="%.4f",
        key="latitude"
    )

    longitude = st.sidebar.number_input(
        "Longitude",
        min_value=94.0,
        max_value=142.0,
        value=float(kota["Longitude"]),
        format="%.4f",
        key="longitude"
    )

    altitude = st.sidebar.number_input(
        "Ketinggian (km)",
        min_value=0.0,
        max_value=850.0,
        value=0.0,
        step=0.1
    )

    tanggal = st.sidebar.date_input(
        "Tanggal Analisis",
        value=date(2026, 11, 18),
        min_value=date(2025, 1, 1),
        max_value=date(2029, 12, 31)
    )

    awal = date(tanggal.year, 1, 1)
    akhir = date(tanggal.year + 1, 1, 1)

    tahun = (
        tanggal.year
        + (tanggal - awal).days
        / (akhir - awal).days
    )

    if st.button("🔍 HITUNG MEDAN MAGNET", type="primary"):

        try:

            hasil = hitung_magnet(
                latitude,
                longitude,
                altitude,
                tahun
            )

            st.success("Perhitungan berhasil!")

            st.subheader("📊 Hasil Perhitungan")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Intensitas Total",
                f"{hasil['F - Intensitas Total (nT)']:,.2f} nT"
            )

            c2.metric(
                "Medan Horizontal",
                f"{hasil['H - Medan Horizontal (nT)']:,.2f} nT"
            )

            c3.metric(
                "Deklinasi",
                f"{hasil['Deklinasi (derajat)']:.2f}°"
            )

            tabel = pd.DataFrame({
                "Parameter": list(hasil.keys()),
                "Hasil": list(hasil.values())
            })

            st.dataframe(
                tabel.round(3),
                use_container_width=True,
                hide_index=True
            )

            csv = tabel.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Hasil Perhitungan",
                csv,
                "hasil_medan_magnet.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Perhitungan gagal: {e}")

# =====================================================
# 11. HALAMAN PETA PERSEBARAN
# =====================================================

elif menu == "Peta Persebaran Indonesia":

    st.header("🗺️ PETA PERSEBARAN MEDAN MAGNET INDONESIA")

    st.write("""
    Peta berikut menampilkan estimasi intensitas
    medan magnet bumi pada 20 kota di Indonesia.
    """)

    tahun_peta = st.slider(
        "Tahun Analisis",
        min_value=2025.0,
        max_value=2029.9,
        value=2026.0,
        step=0.1
    )

    try:

        df_hasil = hitung_seluruh_kota(tahun_peta)

        fig = px.scatter_geo(
            df_hasil,
            lat="Latitude",
            lon="Longitude",
            color="F - Intensitas Total (nT)",
            hover_name="Kota",
            hover_data=[
                "F - Intensitas Total (nT)",
                "H - Medan Horizontal (nT)",
                "Deklinasi (derajat)"
            ],
            color_continuous_scale="Turbo",
            projection="mercator",
            title="Persebaran Intensitas Medan Magnet Indonesia"
        )

        fig.update_geos(
            lonaxis_range=[94, 142],
            lataxis_range=[-12, 8],
            showcountries=True,
            showland=True,
            landcolor="rgb(235,235,235)",
            showocean=True,
            oceancolor="rgb(220,235,250)"
        )

        fig.update_layout(height=650)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("📈 Grafik Perbandingan Antar Kota")

        fig_bar = px.bar(
            df_hasil.sort_values(
                "F - Intensitas Total (nT)",
                ascending=False
            ),
            x="Kota",
            y="F - Intensitas Total (nT)",
            color="F - Intensitas Total (nT)",
            color_continuous_scale="Viridis"
        )

        fig_bar.update_layout(
            xaxis_tickangle=-45,
            height=500
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

        st.subheader("📋 Tabel Data Medan Magnet")

        st.dataframe(
            df_hasil.round(3),
            use_container_width=True,
            hide_index=True
        )

        csv = df_hasil.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Seluruh Data CSV",
            csv,
            "data_medan_magnet_indonesia.csv",
            "text/csv"
        )

    except Exception as e:
        st.error(f"Gagal menampilkan peta: {e}")

# =====================================================
# 12. HALAMAN CONTOH SOAL
# =====================================================

elif menu == "Contoh Soal":

    st.header("📝 CONTOH SOAL MEDAN MAGNET")

    st.subheader("Soal 1: Medan Magnet pada Kawat Lurus")

    st.write("""
    Sebuah kawat lurus panjang dialiri arus listrik
    sebesar 5 A. Tentukan besar medan magnet pada
    titik yang berjarak 0,1 m dari kawat!
    """)

    with st.expander("Lihat Pembahasan Soal 1"):

        st.write("Diketahui:")

        st.latex(r"I = 5 \ A")

        st.latex(r"r = 0,1 \ m")

        st.latex(r"\mu_0 = 4\pi \times 10^{-7} \ Tm/A")

        st.write("Ditanya: B = ?")

        st.write("Penyelesaian:")

        st.latex(
            r"B = \frac{\mu_0 I}{2\pi r}"
        )

        st.latex(
            r"B = \frac{4\pi \times 10^{-7}\times 5}"
            r"{2\pi \times 0,1}"
        )

        st.latex(
            r"B = 1 \times 10^{-5} \ T"
        )

        st.success(
            "Jadi, besar medan magnet adalah 1 × 10⁻⁵ Tesla."
        )

    st.divider()

    st.subheader("Soal 2: Hubungan Komponen Medan Magnet Bumi")

    st.write("""
    Pada suatu lokasi, diketahui komponen medan magnet
    arah utara sebesar 30.000 nT dan komponen arah timur
    sebesar 4.000 nT. Hitung medan horizontalnya!
    """)

    with st.expander("Lihat Pembahasan Soal 2"):

        st.write("Diketahui:")

        st.latex(r"X = 30.000 \ nT")

        st.latex(r"Y = 4.000 \ nT")

        st.write("Penyelesaian:")

        st.latex(r"H = \sqrt{X^2 + Y^2}")

        st.latex(
            r"H = \sqrt{30.000^2 + 4.000^2}"
        )

        st.latex(
            r"H = \sqrt{916.000.000}"
        )

        st.latex(
            r"H \approx 30.265,49 \ nT"
        )

        st.success(
            "Jadi, medan horizontal sekitar 30.265,49 nT."
        )

    st.divider()

    st.subheader("Soal 3: Intensitas Total Medan Magnet")

    st.write("""
    Diketahui medan horizontal suatu lokasi sebesar
    30.000 nT dan komponen vertikal sebesar 40.000 nT.
    Tentukan intensitas total medan magnet!
    """)

    with st.expander("Lihat Pembahasan Soal 3"):

        st.latex(r"F = \sqrt{H^2 + Z^2}")

        st.latex(
            r"F = \sqrt{30.000^2 + 40.000^2}"
        )

        st.latex(
            r"F = 50.000 \ nT"
        )

        st.success(
            "Jadi, intensitas total medan magnet adalah 50.000 nT."
        )

# =====================================================
# 13. HALAMAN TENTANG APLIKASI
# =====================================================

elif menu == "Tentang Aplikasi":

    st.header("ℹ️ TENTANG APLIKASI")

    st.subheader("1. Deskripsi Aplikasi")

    st.write("""
    Deteksi Medan Magnet Indonesia merupakan aplikasi
    berbasis web yang dikembangkan menggunakan Python
    dan Streamlit untuk menghitung serta memvisualisasikan
    estimasi medan magnet bumi di berbagai wilayah Indonesia.

    Aplikasi ini memanfaatkan model World Magnetic Model
    2025 (WMM-2025) untuk memperoleh komponen medan magnet
    berdasarkan koordinat geografis, ketinggian, dan waktu.
    """)

    st.divider()

    st.subheader("2. Fitur Aplikasi")

    st.markdown("""
    - Materi pembelajaran mengenai medan magnet.
    - Penjelasan pengertian dan rumus medan magnet.
    - Contoh penerapan medan magnet dalam kehidupan.
    - Perhitungan medan magnet berdasarkan koordinat.
    - Visualisasi peta persebaran Indonesia.
    - Grafik perbandingan intensitas medan magnet.
    - Tabel komponen medan magnet.
    - Unduh hasil perhitungan dalam format CSV.
    - Contoh soal dan pembahasan.
    """)

    st.divider()

    st.subheader("3. Teknologi yang Digunakan")

    teknologi = pd.DataFrame({
        "Teknologi": [
            "Python",
            "Streamlit",
            "Pandas",
            "NumPy",
            "Plotly",
            "PyGeoMag",
            "WMM-2025"
        ],

        "Kegunaan": [
            "Bahasa pemrograman utama",
            "Membangun aplikasi web interaktif",
            "Pengolahan data",
            "Komputasi numerik",
            "Visualisasi grafik dan peta",
            "Perhitungan medan geomagnetik",
            "Model medan magnet bumi"
        ]
    })

    st.dataframe(
        teknologi,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("4. Sumber Model")

    st.write("""
    Perhitungan medan magnet dalam aplikasi ini menggunakan
    World Magnetic Model 2025 (WMM-2025).

    WMM-2025 dikembangkan melalui kerja sama lembaga
    National Centers for Environmental Information (NCEI),
    British Geological Survey (BGS), dan lembaga terkait.

    Model ini digunakan untuk menghitung komponen utama
    medan magnet bumi berdasarkan posisi dan waktu.
    """)

    st.markdown(
        "[NOAA - World Magnetic Model](https://www.ncei.noaa.gov/products/world-magnetic-model)"
    )

    st.markdown(
        "[Dokumentasi PyGeoMag](https://pygeomag.readthedocs.io/en/latest/)"
    )

    st.divider()

    st.subheader("5. Catatan dan Keterbatasan")

    st.warning("""
    1. Aplikasi menggunakan estimasi model WMM-2025,
       bukan pengukuran langsung menggunakan sensor magnetometer.

    2. Model WMM-2025 berlaku untuk periode 2025–2030,
       dengan tanggal valid sampai 31 Desember 2029.

    3. Peta persebaran hanya menggunakan 20 kota sampel
       di Indonesia, sehingga belum mewakili setiap titik
       geografis di seluruh wilayah Indonesia.

    4. Hasil perhitungan dapat berbeda dengan pengukuran
       langsung karena adanya variasi medan magnet lokal,
       kondisi geologi, dan gangguan geomagnetik.

    5. Ketinggian pada input dinyatakan dalam kilometer
       sesuai parameter altitude yang digunakan PyGeoMag.

    6. Aplikasi ini ditujukan sebagai media pembelajaran
       dan eksplorasi data geomagnetik.
    """)

    st.divider()

    st.subheader("6. Kesimpulan")

    st.write("""
    Melalui aplikasi ini, pengguna dapat mempelajari
    konsep medan magnet bumi sekaligus mengamati
    variasi estimasi medan magnet di wilayah Indonesia.
    Integrasi materi fisika, perhitungan numerik,
    grafik, dan peta interaktif diharapkan dapat
    membantu meningkatkan pemahaman terhadap
    fenomena geomagnetik.
    """)

# =====================================================
# 14. FOOTER
# =====================================================

st.divider()

st.caption("""
🧲 DETEKSI MEDAN MAGNET INDONESIA

Dikembangkan menggunakan Python, Streamlit,
Plotly, dan model geomagnetik WMM-2025.

Media pembelajaran dan visualisasi fisika.
""")
