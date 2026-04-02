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

    # Cek apakah data hari ini sudah ada
    if os.path.exists(output):
        print(f"[INGEST] Data hari ini sudah ada: {output}")
        print(f"[INGEST] Melewati proses ingestion.")
        return output

    # Cek apakah file sumber tersedia
    if not os.path.exists(RAW_DATA_SOURCE):
        print(f"[ERROR] File sumber tidak ditemukan: {RAW_DATA_SOURCE}")
        print(f"[INFO]  Pastikan tiketcom_bestprice.csv ada di folder data/raw/")
        return None

    # Load data asli
    df = pd.read_csv(RAW_DATA_SOURCE, sep='|')

    # Simulasi variasi harga harian (noise kecil)
    np.random.seed(int(today))
    noise = np.random.uniform(-0.03, 0.03, len(df))
    df['best_price'] = df['best_price'] * (1 + noise)
    df['best_price'] = df['best_price'].round(0)

    # Tambahkan timestamp pengambilan data
    df['ingest_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simpan
    df.to_csv(output, index=False)
    print(f"[INGEST] ✅ Data berhasil disimpan: {output}")
    print(f"[INGEST] Jumlah baris: {len(df)}")

    # Simpan log metadata
    log = {
        "ingest_timestamp" : timestamp,
        "source_file"      : RAW_DATA_SOURCE,
        "output_file"      : output,
        "total_rows"       : len(df),
        "columns"          : list(df.columns),
        "status"           : "success"
    }
    log_path = f"{LOG_DIR}/log_{timestamp}.json"
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"[INGEST] Log tersimpan: {log_path}")

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
