import mlflow.pyfunc
import pandas as pd

# 1. Tentukan URI model berdasarkan stage Production
model_name = "Flight_Price_XGBoost_Model"
stage = "Production"
model_uri = f"models:/{model_name}/{stage}"

print(f"Memuat model dari: {model_uri}...")

try:
    # 2. Load model secara otomatis dari Registry
    model = mlflow.pyfunc.load_model(model_uri)

    # 3. Simulasi data input berdasarkan Feature Engineering
    # Contoh skenario: Keberangkatan Bulan Mei (Liburan), Hari Sabtu (Weekend), 
    # Kode asal: 0 (misal CGK), Kode tujuan: 1 (misal DPS)
    
    data = [[4, 6, 1, 1, 0, 22]] # Nilai input
    cols = [
        'bulan', 
        'hari_minggu', 
        'is_weekend', 
        'is_holiday', 
        'origin_enc', 
        'dest_enc'
    ] 
    
    input_df = pd.DataFrame(data, columns=cols)
    print("\nData yang akan diinferensi:")
    print(input_df.to_string(index=False))

    # 4. Prediksi
    prediction = model.predict(input_df)
    
    # Berdasarkan definisi LK-03 (Asumsi: 1 = BELI SEKARANG, 0 = TUNGGU)
    hasil_teks = "BELI SEKARANG" if prediction[0] == 1 else "TUNGGU"
    
    print(f"\n Verifikasi Berhasil! Hasil Prediksi: {hasil_teks}")

except Exception as e:
    print(f" Gagal memuat model: {e}")
    print("Pastikan nama model dan stage di MLflow Registry sudah benar.")