import plotly.express as px
import pandas as pd
import random
import os
import cv2
import numpy as np
from PIL import Image
import streamlit as st
import plotly.graph_objects as go
from scipy import stats


def apply_hud_layout(fig):
    """Menerapkan tema Tactical HUD ke grafik Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="'Inter', sans-serif",
        font_color="#64748B",
        title_font_color="#0B4A8E",
        title_font_size=15,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False, zeroline=False, tickcolor="#CBD5E1", linecolor="#CBD5E1"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, tickcolor="#CBD5E1")
    )
    return fig

def plot_severity_distribution(df: pd.DataFrame):
    fig = px.histogram(
        df, x="severity_score", nbins=40, 
        color="pothole_size_category",
        title="Distribusi Keparahan Kerusakan (Severity Index)",
        color_discrete_map={'Small': '#93C5FD', 'Medium': '#FACC15', 'Large': '#F87171'},
        opacity=0.9
    )
    fig.update_traces(marker_line_width=0, hovertemplate="<b>SEV_SCORE:</b> %{x}<br><b>COUNT:</b> %{y}<extra></extra>")
    return apply_hud_layout(fig)

def plot_spatial_radar(df: pd.DataFrame):
    """Menyulap 2D Histogram menjadi seperti Radar Thermal"""
    # Mencegah Pandas SettingWithCopyWarning saat menerima data hasil filter
    df_radar = df.copy() 
    
    df_radar['norm_x'] = df_radar['center_x'] / df_radar['width']
    df_radar['norm_y'] = 1 - (df_radar['center_y'] / df_radar['height'])
    
    fig = px.density_heatmap(
        df_radar, x="norm_x", y="norm_y", 
        title="Peta Kepadatan Spasial (In-Frame)",
        nbinsx=25, nbinsy=25,
        color_continuous_scale="Blues"
    )
    fig = apply_hud_layout(fig)
    fig.update_xaxes(range=[0, 1], showgrid=False, title="Posisi X")
    fig.update_yaxes(range=[0, 1], showgrid=False, title="Posisi Y")
    return fig

def plot_data_split(df: pd.DataFrame):
    # Logika aggregasi paling aman agar tidak crash dengan Pylance atau Pandas versi lama
    split_counts = df.groupby(['split', 'pothole_size_category'])['image_name'].count().reset_index()
    split_counts.rename(columns={'image_name': 'count'}, inplace=True)
    
    fig = px.bar(
        split_counts, x="split", y="count", color="pothole_size_category",
        title="Topologi Machine Learning Split",
        barmode="group",
        color_discrete_map={'Small': '#93C5FD', 'Medium': '#FACC15', 'Large': '#F87171'}
    )
    fig.update_traces(marker_line_width=0, hovertemplate="<b>SPLIT:</b> %{x}<br><b>VOL:</b> %{y} NODES<extra></extra>")
    return apply_hud_layout(fig)

def display_image_samples(img_dir, num_samples=3):
    """Menampilkan grid gambar secara acak dari direktori (Fallback Method)"""
    if not os.path.exists(img_dir):
        st.warning(f"[SYS_ERR]: DIRECTORY_NOT_FOUND: {img_dir}")
        return
        
    all_imgs = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not all_imgs:
        st.warning(f"[SYS_ERR]: NO_IMAGES_FOUND_IN: {img_dir}")
        return

    samples = random.sample(all_imgs, min(num_samples, len(all_imgs)))
    
    cols = st.columns(num_samples)
    for i, img_name in enumerate(samples):
        img_path = os.path.join(img_dir, img_name)
        try:
            image = Image.open(img_path)
            with cols[i]:
                st.image(image, caption=f"> ID: {img_name}", width='stretch')
                st.markdown(f"<p style='font-family:monospace; font-size:0.6rem; color:#666;'>RES: {image.size[0]}x{image.size[1]}px</p>", unsafe_allow_html=True)
        except Exception:
            st.error(f"[SYS_ERR]: CORRUPTED_IMAGE {img_name}")

def display_image_with_bboxes(df_metadata, img_dir, num_samples=2):
    """Menampilkan gambar lengkap dengan Bounding Box yang digambar secara LIVE"""
    if not os.path.exists(img_dir):
        st.warning(f"[SYS_ERR]: DIRECTORY_NOT_FOUND: {img_dir}")
        return
        
    # Ambil sampel gambar yang ada di folder DAN ada di metadata yang sudah di-filter
    available_imgs = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    valid_samples = df_metadata[df_metadata['image_name'].isin(available_imgs)]['image_name'].unique()
    
    if len(valid_samples) == 0:
        st.info("Tidak ada sampel gambar yang sesuai dengan filter saat ini.")
        return

    samples = random.sample(list(valid_samples), min(num_samples, len(valid_samples)))
    
    cols = st.columns(num_samples)
    for i, img_name in enumerate(samples):
        img_path = os.path.join(img_dir, img_name)
        img_array = cv2.imread(img_path)
        
        if img_array is None:
            st.warning(f"[SYS_ERR]: FAILED_TO_LOAD_IMAGE: {img_path}")
            continue

        # Konversi ke RGB agar warna tepat di Streamlit
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        
        # Tarik semua Bounding Box untuk gambar ini dari dataframe
        bboxes = df_metadata[df_metadata['image_name'] == img_name]
        
        for _, row in bboxes.iterrows():
            try:
                # Memastikan tipe data valid untuk diproses OpenCV
                xmin, ymin = int(float(row['xmin'])), int(float(row['ymin']))
                xmax, ymax = int(float(row['xmax'])), int(float(row['ymax']))
                sev_score = float(row['severity_score'])
            except (ValueError, TypeError):
                continue
                
            # Gambar kotak Ink Blue
            cv2.rectangle(
                img_array, 
                (xmin, ymin), 
                (xmax, ymax), 
                (11, 74, 142), 3 
            )
            
            # Tulis text severity score di atas kotak 
            text = f" SEV: {sev_score:.1f} "
            text_y = max(15, ymin - 8)
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            
            cv2.rectangle(img_array, (xmin, text_y - th - 4), (xmin + tw + 4, text_y + 4), (250, 204, 21), -1)
            cv2.putText(
                img_array, text, 
                (xmin + 2, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (11, 74, 142), 1, cv2.LINE_AA
            )
            
        with cols[i]:
            st.image(img_array, caption=f"> ID: {img_name}", width='stretch')

def plot_data_funnel(original_count, cleaned_count):
    """Grafik penyusutan data untuk halaman Data Purification"""
    fig = go.Figure(go.Funnel(
        y=["DATA MENTAH KAGGLE", "LOLOS FILTER LAPLACIAN"],
        x=[original_count, cleaned_count],
        textinfo="value+percent initial",
        marker={"color": ["#93C5FD", "#0B4A8E"]}
    ))
    fig.update_layout(title="ALUR PEMBERSIHAN DATA", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="'Inter', sans-serif", font_color="#64748B")
    return fig

def perform_ab_test(df: pd.DataFrame):
    """Menjalankan A/B Testing (T-Test) antara Train dan Test set"""
    train_sev = df[df['split'] == 'train']['severity_score'].dropna()
    test_sev = df[df['split'] == 'test']['severity_score'].dropna()
    
    if len(train_sev) < 2 or len(test_sev) < 2:
        return None, None
        
    t_stat, p_value = stats.ttest_ind(train_sev, test_sev, equal_var=False)
    return t_stat, p_value