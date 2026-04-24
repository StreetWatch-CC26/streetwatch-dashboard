import streamlit as st

def render_hud_metric(title: str, value: str, status_color: str = "green", extra_info: str = ""):
    status_class = "status-green" if status_color == "green" else "status-red"
    
    html_content = f"""
    <div class="hud-card">
        <div class="hud-title">
            <span class="status-indicator {status_class}"></span> {title}
        </div>
        <div class="hud-metric">{value}</div>
        <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #64748B; margin-top: 10px; font-weight: 500;">
            {extra_info}
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def render_terminal_header(title: str, subtitle: str):
    html = f"""
    <div style="margin-bottom: 2rem; border-bottom: 1.5px dashed #E2E8F0; padding-bottom: 1rem;">
        <h1 style="font-family: 'Inter', sans-serif; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em; color: #0B4A8E; margin-bottom: 0.25rem;">
            {title}
        </h1>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.95rem; color: #64748B;">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_hud_metric_with_delta(title, value, delta, status="green"):
    status_class = "status-green" if status == "green" else "status-red"
    delta_color = "#10B981" if "-" in delta or "+" in delta else "#64748B"
    
    html = f"""
    <div class="hud-card">
        <div class="hud-title"><span class="status-indicator {status_class}"></span> {title}</div>
        <div class="hud-metric">{value}</div>
        <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: {delta_color}; margin-top: 8px; font-weight: 600;">
            {delta}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def nerd_mode_viewer(label, code_content):
    with st.expander(f"🔍 Lihat Kode Algoritma: {label}", expanded=False):
        st.code(code_content, language='python')