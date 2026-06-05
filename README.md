# 🛣️ StreetWatch Dashboard: Road Damage Data Intelligence

StreetWatch Dashboard adalah aplikasi analitik berbasis Streamlit yang digunakan untuk menganalisis dataset deteksi jalan berlubang atau pothole. Dashboard ini membantu pengguna memahami kualitas data, tingkat keparahan kerusakan jalan, distribusi posisi lubang pada gambar, serta kesiapan dataset untuk pengembangan model Computer Vision.

## 📌 Project Overview

Kerusakan jalan merupakan salah satu masalah infrastruktur yang berdampak langsung pada keselamatan dan kenyamanan pengguna jalan. Namun, proses pelaporan dan analisis kerusakan jalan sering kali masih dilakukan secara manual dan belum berbasis data.

StreetWatch Dashboard dikembangkan untuk membantu proses analisis data pothole melalui pendekatan Data Science, mulai dari eksplorasi data, quality control, visualisasi, hingga validasi statistik dataset.

Project ini membantu pengguna untuk:

* Memahami distribusi tingkat keparahan jalan berlubang
* Mengidentifikasi data gambar yang kurang layak digunakan
* Melihat pola posisi pothole di dalam frame gambar
* Menganalisis pembagian data training dan testing
* Memvalidasi keseimbangan dataset menggunakan pengujian statistik
* Mengekspor data pothole kritis untuk kebutuhan simulasi maintenance dispatch

## 🚀 Features

### 📊 Dashboard Overview

Menampilkan ringkasan utama dari dataset pothole dalam bentuk visualisasi interaktif, meliputi:

* Total anomali pothole
* Jumlah kasus kritis
* Rata-rata severity score
* Distribusi tingkat keparahan pothole
* Catatan analitik terkait kondisi data

### 🧹 Data Purification

Fitur ini digunakan untuk melakukan quality control terhadap gambar pothole.

Proses penyaringan dilakukan menggunakan metode Variance of Laplacian untuk mendeteksi gambar yang buram. Gambar dengan kualitas rendah dapat memengaruhi performa model Computer Vision, sehingga perlu diidentifikasi sebelum masuk ke tahap pelatihan model.

Analisis yang ditampilkan:

* Jumlah data mentah
* Jumlah data yang lolos filter
* Jumlah data buram yang dibuang
* Ambang batas Laplacian
* Bukti visual data yang lolos uji kualitas

### 🗺️ Spatial Recon

Menganalisis distribusi posisi pothole di dalam gambar berdasarkan koordinat bounding box.

Fitur ini membantu melihat apakah data memiliki kecenderungan posisi tertentu, misalnya pothole lebih sering muncul di area tengah-bawah gambar. Informasi ini penting untuk mendeteksi potensi bias pada dataset sebelum digunakan dalam pelatihan model AI.

### 🤖 AI Pipeline

Menampilkan struktur pembagian dataset untuk kebutuhan machine learning.

Fitur ini mencakup:

* Distribusi data training dan testing
* Informasi data uji
* Simulasi augmentasi sintetis
* Visualisasi hasil augmentasi gambar
* Raw data dump untuk melihat sampel data secara langsung

Augmentasi digunakan untuk membantu model lebih tahan terhadap berbagai kondisi lapangan, seperti perubahan pencahayaan, noise kamera, dan rotasi gambar.

### 🧪 Statistical Testing

Fitur ini digunakan untuk memvalidasi keseimbangan distribusi dataset menggunakan Welch’s T-Test.

Pengujian dilakukan untuk membandingkan rata-rata severity score antara data training dan testing.

Hipotesis yang digunakan:

* H0: Tidak ada perbedaan signifikan antara data training dan testing
* H1: Terdapat perbedaan signifikan antara data training dan testing

Jika p-value lebih besar dari 0.05, maka pembagian dataset dianggap cukup seimbang.

### 📥 Export Maintenance Dispatch

Dashboard menyediakan fitur export data pothole kritis dalam format CSV.

Data yang diekspor dapat digunakan untuk simulasi prioritas perbaikan jalan atau maintenance dispatch berdasarkan severity score.

## 📂 Dataset

Dataset yang digunakan berasal dari Kaggle:

[Andrew Mvd - Pothole Detection Dataset](https://www.kaggle.com/datasets/andrewmvd/pothole-detection/data)

Dataset ini berisi gambar jalan dengan anotasi pothole. Pada project ini, dataset diproses menjadi data tabular dan diperkaya dengan beberapa fitur hasil feature engineering.

Beberapa fitur yang digunakan:

* image_name
* width
* height
* xmin
* ymin
* xmax
* ymax
* bbox_width
* bbox_height
* bbox_area
* image_area
* severity_score
* pothole_size_category
* blur_score
* split

## 🧠 Severity Score

Severity Score digunakan untuk mengukur tingkat keparahan pothole berdasarkan ukuran relatif lubang terhadap area gambar.

Semakin besar area pothole pada gambar, semakin tinggi nilai severity score yang dihasilkan.

Kategori analisis yang digunakan:

* Small
* Medium
* Large

Pothole dengan severity score tinggi dikategorikan sebagai prioritas kritis karena berpotensi membutuhkan tindakan perbaikan lebih cepat.

## 🏗️ Data Science Pipeline

Alur pengerjaan project ini meliputi:

1. Mengambil dataset pothole dari Kaggle
2. Membaca data gambar dan anotasi bounding box
3. Mengubah data anotasi menjadi format tabular
4. Melakukan feature engineering pada ukuran pothole
5. Menghitung severity score
6. Mengukur kualitas gambar menggunakan blur score
7. Membagi dataset ke dalam data training dan testing
8. Melakukan visualisasi data dengan Streamlit
9. Melakukan pengujian statistik untuk validasi dataset

## 🛠️ Technologies Used

Project ini dikembangkan menggunakan:

* Python
* Streamlit
* Pandas
* Plotly
* OpenCV
* Pillow
* SciPy

## 📦 Installation

Clone repository:

```bash
git clone <repository-url>
cd streetwatch-dashboard
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install streamlit pandas plotly opencv-python-headless pillow scipy
```

Jika menggunakan `uv`, jalankan:

```bash
uv sync
```

## ▶️ Run Application

Jalankan aplikasi Streamlit:

```bash
streamlit run app.py
```

Setelah dijalankan, dashboard akan terbuka melalui browser.

## 📁 Project Structure

```text
streetwatch-dashboard/
│
├── .streamlit/
├── assets/
│   └── style.css
│
├── data/
│   ├── pothole_dataset_full.csv
│   ├── images/
│   └── augmented_images/
│
├── src/
│   ├── data_loader.py
│   ├── components.py
│   └── visualizations.py
│
├── tests/
├── app.py
├── pyproject.toml
├── uv.lock
├── StreetWatch_DS.ipynb
└── README.md
```

## 👥 Team

Developed by:

* Della
* Alif

## 📌 Project Status

Project ini berfokus pada tahap Data Science Dashboard untuk analisis dataset pothole. Pengembangan selanjutnya dapat mencakup integrasi model object detection, deployment dashboard, dan sistem pelaporan kerusakan jalan berbasis AI.

## 📄 License

Project ini dibuat untuk kebutuhan pembelajaran, portofolio, dan pengembangan project Data Science.
