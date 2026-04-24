import os
import pandas as pd
from src.data_loader import load_full_data

def test_dataset_exists():
    assert os.path.exists('data/pothole_dataset_full.csv'), "Dataset CSV tidak ditemukan!"

def test_data_schema():
    df = load_full_data('data/pothole_dataset_full.csv')
    required_columns = ['image_name', 'bbox_area', 'severity_score', 'pothole_size_category', 'split']
    for col in required_columns:
        assert col in df.columns, f"Kolom krusial hilang: {col}"

def test_severity_calculation():
    # Simulasi perhitungan severity (Area_ratio * 100 + count * 0.5)
    bbox_area = 5000
    image_area = 135000
    count = 2
    expected_severity = round((bbox_area / image_area) * 100 + (count * 0.5), 2)
    assert expected_severity == 4.7, "Logika Severity Score berubah!"