import os
import shutil
import json
import pandas as pd
import numpy as np
from datetime import datetime

RAW_DATA_SOURCE = "data/raw/tiketcom_bestprice.csv"
RAW_DATA_DIR    = "data/raw"
LOG_DIR         = "data/raw/logs"

def ingest_data():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    today     = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output    = f"{RAW_DATA_DIR}/tiketcom_{today}.csv"

    if not os.path.exists(RAW_DATA_SOURCE):
        print(f"[ERROR] File sumber tidak ditemukan: {RAW_DATA_SOURCE}")
        return None

    # Load data asli
    df = pd.read_csv(RAW_DATA_SOURCE, sep='|')
    
    # Random seed berdasarkan jam agar selalu berbeda tiap kali dijalankan
    np.random.seed(int(datetime.now().timestamp()))
    noise = np.random.uniform(-0.03, 0.03, len(df))
    df['best_price'] = df['best_price'] * (1 + noise)
    df['best_price'] = df['best_price'].round(0)
    df['ingest_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # SIMULASI CONTINUAL LEARNING: Jika file sudah ada, tambahkan data ke dalamnya
    if os.path.exists(output):
        print(f"[INGEST] File hari ini sudah ada. Melakukan Continual Learning (Append data baru)...")
        # Ambil 50 baris acak sebagai data baru yang masuk
        new_data = df.sample(n=50) 
        # Gabungkan data lama dengan data baru
        existing_df = pd.read_csv(output)
        df_final = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        df_final = df

    # Simpan
    df_final.to_csv(output, index=False)
    print(f"[INGEST] ✅ Data berhasil disimpan: {output}")
    print(f"[INGEST] Jumlah baris saat ini: {len(df_final)}")

    return output

if __name__ == "__main__":
    print("=" * 50)
    print("DATA INGESTION — Flight Price Prediction")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")
    result = ingest_data()
    if result:
        print(f"\n Ingestion selesai: {result}")
    else:
        print("\n Ingestion gagal.")
