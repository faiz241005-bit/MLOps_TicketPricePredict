import mlflow.pyfunc
import pandas as pd
import numpy as np

# 1. Load Model dari Registry
model_uri = "models:/Flight_Price_XGBoost_Model/Production"
print("Memuat model...")
model = mlflow.pyfunc.load_model(model_uri)

# 2. Load Dataset Processed
print("Memuat dataset...")
df = pd.read_csv("data/processed/tiketcom_20260402_feat.csv", sep='|' if '|' in open("data/processed/tiketcom_20260402_feat.csv").readline() else ',')

# 3. Pilih fitur yang sesuai
cols = ['bulan', 'hari_minggu', 'is_weekend', 'is_holiday', 'origin_enc', 'dest_enc']
X = df[cols]

# 4. Lakukan prediksi pada SELURUH data
print("Mencari pola TUNGGU di ribuan data...")
prediksi_semua = model.predict(X)

# 5. Cari index yang hasilnya 0 (TUNGGU)
index_tunggu = np.where(prediksi_semua == 0)[0]

if len(index_tunggu) > 0:
    print(f"\n Berhasil! Ditemukan {len(index_tunggu)} baris data dengan prediksi TUNGGU.")
    print("Berikut adalah 3 contoh teratas:\n")
    
    contoh_data = X.iloc[index_tunggu[:3]]
    print(contoh_data.to_string(index=False))
    
    # Ambil baris pertama dan jadikan format list Python
    nilai_list = contoh_data.iloc[0].values.tolist()
    
    print(f"\n=== COPY KODE INI KE verify_inference.py ===")
    print(f"data = [{nilai_list}]")
else:
    print("\n Tidak ditemukan prediksi 0 di seluruh dataset.")
    print("Cek kembali apakah data Anda benar-benar memiliki label 0 saat training.")