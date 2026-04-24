import streamlit as st
import pandas as pd
from src.data_loader import load_full_data
from src.components import render_hud_metric, render_terminal_header, render_hud_metric_with_delta, nerd_mode_viewer
import src.visualizations as viz

st.set_page_config(page_title="StreetWatch Analytics", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

raw_df = load_full_data('data/pothole_dataset_full.csv')
if raw_df.empty:
    st.error("[ERROR]: DATA_CORRUPTION. MISSING_CSV_FILES.")
    st.stop()

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Inter', sans-serif; font-weight: 800; color: #0B4A8E; margin-bottom: 0; font-size: 1.8rem; letter-spacing: -0.05em;">StreetWatch</h2>
        <p style="font-family: 'Inter', sans-serif; color: #64748B; font-size: 0.9rem; margin-top:0;">Data Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("MAIN_MENU", [
        "01 Overview", 
        "02 Data Purification", 
        "03 Spatial Recon", 
        "04 AI Pipeline",
        "05 Statistical Testing"
    ], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    nerd_mode = st.toggle("Tampilkan Source Code", value=False)
    
    st.markdown("<hr style='border-top: 1.5px dashed #CBD5E1;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: Inter, sans-serif; color: #0B4A8E; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;'>Filter Global</p>", unsafe_allow_html=True)
    
    min_sev = st.slider("Minimum Keparahan", min_value=0.0, max_value=float(raw_df['severity_score'].max()), value=0.0, step=1.0)
    selected_sizes = st.multiselect("Ukuran Kerusakan", ['Small', 'Medium', 'Large'], default=['Small', 'Medium', 'Large'])
    
    df = raw_df[(raw_df['severity_score'] >= min_sev) & (raw_df['pothole_size_category'].isin(selected_sizes))]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    critical_data = raw_df[raw_df['severity_score'] > 20.0].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="↓ Export Maintenance Dispatch",
        data=critical_data,
        file_name='critical_potholes_dispatch.csv',
        mime='text/csv',
        type="primary",
        width='stretch'
    )
    
    st.markdown("<br><p style='font-family: Inter, sans-serif; color: #94A3B8; font-size: 0.7rem;'>Tim Pengembang: Della & Alif</p>", unsafe_allow_html=True)

# Page 1: Overview
if page == "01 Overview":
    render_terminal_header("Ringkasan Eksekutif", "Ikhtisar volume kerusakan infrastruktur dan metrik keparahan secara komprehensif.")
    
    total_anomalies = len(df)
    critical_cases = len(df[df['severity_score'] > 20.0])
    avg_sev = f"{df['severity_score'].mean():.2f}" if not df.empty else "0.00"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_hud_metric("TOTAL ANOMALI", f"{total_anomalies:,}", "green", "Titik Terverifikasi")
    with col2:
        render_hud_metric("PRIORITAS KRITIS", f"{critical_cases:,}", "red", "Severity > 20.0")
    with col3:
        render_hud_metric("AVG SEVERITY", avg_sev, "green", "Ambang Batas Aman: < 15.0")
        
    c1, c2 = st.columns([2, 1])
    with c1:
        if not df.empty:
            st.plotly_chart(viz.plot_severity_distribution(df), width='stretch')
        else:
            st.warning("Data tidak mencukupi untuk visualisasi.")
    with c2:
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title"><span class="status-indicator status-green"></span> Catatan Analitik</div>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
            Sistem mendeteksi distribusi anomali aspal jalan raya. Alokasi perbaikan difokuskan pada lubang dengan klasifikasi 'Large' dan memiliki <i>Severity Score</i> ekstrem.<br><br>
            Tingkat keparahan ini dikalkulasi berdasarkan rasio luas lubang terhadap area pandang kamera.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Page 2: IQA & Data Purification
elif page == "02 Data Purification":
    render_terminal_header("Quality Control (IQA)", "Penyaringan data berkualitas rendah menggunakan deteksi tepi Laplacian.")
    
    original_total = 1740 
    cleaned_total = len(df)
    dropped = original_total - cleaned_total

    tab1, tab2 = st.tabs(["Metrik & Identifikasi Risiko", "Bukti Visual & Alur Data"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            render_hud_metric_with_delta("DATA MENTAH", f"{original_total:,}", "Sumber: Kaggle")
        with c2:
            render_hud_metric_with_delta("LOLOS FILTER", f"{cleaned_total:,}", f"-{dropped} data buram dihapus", "green")
        with c3:
            render_hud_metric_with_delta("AMBANG LAPLACIAN", "100.0", "Variance of Laplacian")
        
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title"><span class="status-indicator status-red"></span> Identifikasi Risiko: Gambar Buram</div>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
            Model <i>Computer Vision</i> rentan mengalami <i>overfitting</i> jika dilatih menggunakan data laporan masyarakat yang tidak fokus akibat guncangan.<br><br>
            <b>Solusi Rekayasa:</b> Modul IQA menghitung ketajaman tepi piksel. Gambar dengan skor Laplacian di bawah 100.0 secara otomatis dibuang dari dataset latih.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if nerd_mode:
            nerd_mode_viewer("Algoritma Laplacian", """
def calculate_blur_score(image_path):
    image = cv2.imread(image_path)
    if image is None: return 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

# EXECUTE FILTER:
valid_images = df_iqa[df_iqa['blur_score'] >= 100.0]['image_name']
            """)

    with tab2:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(viz.plot_data_funnel(original_total, cleaned_total), width='stretch')
        with col2:
            st.markdown("<h3 style='font-family:Inter, sans-serif; color:#0B4A8E; font-size:1rem; font-weight:700;'>Data Bersih Lolos Uji</h3>", unsafe_allow_html=True)
            viz.display_image_with_bboxes(df, 'data/images/test', num_samples=1) 

# Page 3: Spatial Recon
elif page == "03 Spatial Recon":
    render_terminal_header("Distribusi Spasial", "Pemetaan posisi koordinat kerusakan di dalam lensa kamera.")
    
    c1, c2 = st.columns([5, 3])
    with c1:
        if not df.empty:
            st.plotly_chart(viz.plot_spatial_radar(df), width='stretch')
    with c2:
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title"><span class="status-indicator status-green"></span> Analisis Kepadatan</div>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
            Kepadatan tertinggi secara konsisten berada di kuadran <b>tengah-bawah</b>. Ini memvalidasi bahwa mayoritas laporan berasal dari kamera <i>Dashboard</i> kendaraan yang condong melihat aspal di depan kap mobil.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title"><span class="status-indicator status-red"></span> Tindakan Mitigasi AI</div>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
            Untuk menghindari model AI mengalami overfitting dan hanya "menghafal" posisi bawah layar, teknik <i>Advanced Augmentation</i> seperti rotasi dan pergeseran skala diwajibkan pada pipeline pelatihan.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Page 4: AI Pipeline
elif page == "04 AI Pipeline":
    render_terminal_header("Topologi Machine Learning", "Struktur pembagian dataset latih dan injeksi augmentasi sintetis.")
    
    tab_dist, tab_aug, tab_data = st.tabs(["Distribusi Split", "Augmentasi Sintetis", "Raw Data Dump"])
    
    with tab_dist:
        c1, c2 = st.columns([2, 1])
        with c1:
            if not df.empty:
                st.plotly_chart(viz.plot_data_split(df), width='stretch')
        with c2:
            render_hud_metric_with_delta("DATA LATIH", f"{len(df[df['split']=='train']):,}", "Termasuk data augmentasi", "green")
            render_hud_metric_with_delta("DATA UJI (BLIND)", f"{len(df[df['split']=='test']):,}", "15% Proporsi", "red")

    with tab_aug:
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title"><span class="status-indicator status-green"></span> Injeksi Data Sintetis</div>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
            Penerapan <b>Albumentations</b> digunakan untuk mereplikasi kondisi lapangan yang sulit, seperti jalanan malam, gangguan sensor, dan guncangan rotasi.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        viz.display_image_with_bboxes(raw_df, 'data/augmented_images', num_samples=3)
        
        if nerd_mode:
            nerd_mode_viewer("Albumentations Pipeline", """
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.25, p=0.7),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5)
], bbox_params=A.BboxParams(format='pascal_voc', min_area=25.0, min_visibility=0.1))
            """)

    with tab_data:
        if not df.empty:
            test_df = df[df['split']=='test'].head(20).copy()
            
            cols = test_df.columns.tolist()
            front_cols = ['image_name', 'severity_score', 'pothole_size_category']
            for c in front_cols:
                if c in cols: cols.remove(c)
            test_df = test_df[front_cols + cols]
            
            def highlight_severity(val):
                try:
                    v = float(val)
                    if v > 20.0: return 'background-color: #FEE2E2; color: #DC2626; font-weight: bold;'
                    if v > 10.0: return 'background-color: #FEF9C3; color: #D97706; font-weight: bold;'
                    return ''
                except ValueError:
                    return ''
                    
            if 'severity_score' in test_df.columns:
                styled_df = test_df.style.map(highlight_severity, subset=['severity_score'])
                st.dataframe(styled_df, width='stretch', hide_index=True)
            else:
                st.dataframe(test_df, width='stretch', hide_index=True)
        else:
            st.info("Filter Anda tidak menampilkan data uji.")

# Page 5: Statistical Testing
elif page == "05 Statistical Testing":
    render_terminal_header("Pengujian Hipotesis", "Implementasi A/B Testing untuk validasi keseimbangan distribusi.")
    
    st.markdown("""
    <div class="hud-card">
        <div class="hud-title"><span class="status-indicator status-green"></span> Desain Eksperimen</div>
        <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
        <b>Tujuan:</b> Memverifikasi apakah teknik pemisahan acak <i>(Random Split)</i> menghasilkan sebaran tingkat kerumitan (Severity Score) yang adil antara kelompok <b>Training</b> dan <b>Testing</b>.<br><br>
        <b>H0 (Hipotesis Nol):</b> Tidak ada perbedaan yang signifikan secara statistik antara rata-rata kedua kelompok (Data seimbang).<br>
        <b>H1 (Alternatif):</b> Terdapat perbedaan yang signifikan (Indikasi Bias).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    t_stat, p_val = viz.perform_ab_test(df)
    
    if t_stat is not None:
        c1, c2 = st.columns(2)
        with c1:
            render_hud_metric("T-STATISTIC", f"{t_stat:.4f}", "green", "Metode: Welch's T-Test")
        with c2:
            status_color = "red" if p_val < 0.05 else "green"
            conclusion = "H0 DITOLAK (ADA BIAS)" if p_val < 0.05 else "H0 DITERIMA (SEIMBANG)"
            render_hud_metric("P-VALUE", f"{p_val:.4f}", status_color, conclusion)
            
        st.markdown("<br><h3 style='font-family:Inter, sans-serif; color:#0B4A8E; font-weight:800; font-size:1.1rem;'>Kesimpulan Analisis</h3>", unsafe_allow_html=True)
        
        if p_val > 0.05:
            st.markdown("""
            <div class="alert-success">
                <b>Tervalidasi:</b> Nilai P-Value > 0.05 menunjukkan bahwa tingkat kesulitan data uji sepadan dengan data latih. Evaluasi model ke depannya dapat dipercaya.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-error">
                ⚠️ <b>Peringatan:</b> Nilai P-Value < 0.05. Ditemukan potensi bias pada pemisahan data. Disarankan beralih ke metode Stratified Split.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Data tidak mencukupi untuk Pengujian Hipotesis.")