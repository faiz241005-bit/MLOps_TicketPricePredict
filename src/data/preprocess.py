import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

RAW_DATA_DIR      = "data/raw"
INTERIM_DATA_DIR  = "data/interim"
PROCESSED_DATA_DIR = "data/processed"

def get_latest_raw_file():
    files = [f for f in os.listdir(RAW_DATA_DIR) 
             if f.startswith("tiketcom_2") and f.endswith(".csv")]
    if not files:
        return None
    files.sort(reverse=True)
    return f"{RAW_DATA_DIR}/{files[0]}"

def clean_data(filepath):
    os.makedirs(INTERIM_DATA_DIR, exist_ok=True)

    df = pd.read_csv(filepath)
    print(f"[CLEAN] Data awal       : {len(df)} baris")

    before = len(df)
    df = df.drop_duplicates()
    print(f"[CLEAN] Hapus duplikat  : {before - len(df)} baris dihapus")

    df['best_price']  = pd.to_numeric(df['best_price'], errors='coerce')
    df['depart_date'] = pd.to_datetime(df['depart_date'], errors='coerce')

    before = len(df)
    df = df.dropna(subset=['best_price', 'depart_date', 'origin', 'destination'])
    print(f"[CLEAN] Hapus NaN       : {before - len(df)} baris dihapus")

    before = len(df)
    df = df[(df['best_price'] > 50000) & (df['best_price'] < 20000000)]
    print(f"[CLEAN] Filter outlier  : {before - len(df)} baris dihapus")

    today    = datetime.now().strftime("%Y%m%d")
    out_path = f"{INTERIM_DATA_DIR}/tiketcom_{today}_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"[CLEAN] Data bersih  : {out_path} ({len(df)} baris)\n")

    return out_path, len(df)

def build_features(filepath):

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    df = pd.read_csv(filepath)
    df['depart_date'] = pd.to_datetime(df['depart_date'])

    # Fitur temporal
    df['bulan']       = df['depart_date'].dt.month
    df['hari_minggu'] = df['depart_date'].dt.dayofweek
    df['is_weekend']  = (df['hari_minggu'] >= 5).astype(int)

    # Holiday flag — bulan libur nasional Indonesia
    holiday_months    = [1, 3, 4, 5, 6, 7, 8, 12]
    df['is_holiday']  = df['bulan'].isin(holiday_months).astype(int)

    # Encoding bandara
    le = LabelEncoder()
    df['origin_enc'] = le.fit_transform(df['origin'].astype(str))
    df['dest_enc']   = le.fit_transform(df['destination'].astype(str))

    # Label klasifikasi
    median_price = df['best_price'].median()
    df['label']  = (df['best_price'] > median_price).astype(int)

    print(f"[FEATURES] Fitur dibuat : bulan, hari_minggu, is_weekend, is_holiday")
    print(f"[FEATURES] Encoding     : origin_enc, dest_enc")
    print(f"[FEATURES] Median harga : Rp {median_price:,.0f}")
    print(f"[FEATURES] BELI SEKARANG: {df['label'].sum()} baris")
    print(f"[FEATURES] TUNGGU       : {(df['label']==0).sum()} baris")

    # Simpan
    today    = datetime.now().strftime("%Y%m%d")
    out_path = f"{PROCESSED_DATA_DIR}/tiketcom_{today}_feat.csv"
    df.to_csv(out_path, index=False)
    print(f"[FEATURES] Fitur siap: {out_path}\n")

    return out_path, median_price

def run_preprocessing():
    """Jalankan full preprocessing pipeline."""
    print("=" * 50)
    print("PREPROCESSING — Flight Price Prediction")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")

    # Ambil file raw terbaru
    raw_file = get_latest_raw_file()
    if not raw_file:
        print("[ERROR] Tidak ada file raw ditemukan di data/raw/")
        print("[INFO]  Jalankan ingest_data.py terlebih dahulu.")
        return

    print(f"[INFO] File raw terbaru: {raw_file}\n")

    # Cleaning
    print("🧹 TAHAP 1: CLEANING")
    clean_file, clean_rows = clean_data(raw_file)

    # Feature Engineering
    print("⚙️  TAHAP 2: FEATURE ENGINEERING")
    feat_file, median_price = build_features(clean_file)

    print("=" * 50)
    print("PREPROCESSING SELESAI!")
    print(f"   Output: {feat_file}")
    print("=" * 50)

if __name__ == "__main__":
    run_preprocessing()
