import pandas as pd
import streamlit as st

@st.cache_data
def load_full_data(filepath: str) -> pd.DataFrame:
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return pd.DataFrame()