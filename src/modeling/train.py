import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score

# Atur nama eksperimen di MLflow
mlflow.set_experiment("Flight_Price_Prediction_XGBoost")

def train_model(data_path, n_estimators, learning_rate, max_depth):
    """Fungsi untuk melatih model dan mencatat eksperimen ke MLflow"""
    
    print(f"\nMulai eksperimen: n_estimators={n_estimators}, lr={learning_rate}, max_depth={max_depth}")
    
    # 1. Persiapan Data
    try:
        df = pd.read_csv(data_path, sep='|') if '|' in open(data_path).readline() else pd.read_csv(data_path)
        
        # Simulasi pembuatan label jika belum ada
        if 'label' not in df.columns:
            median_price = df['best_price'].median()
            df['label'] = np.where(df['best_price'] > median_price, 1, 0) 
        # Pilih kolom numerik untuk fitur sederhana
        X = df.select_dtypes(include=[np.number]).drop(columns=['label', 'best_price'], errors='ignore')
        y = df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        print(f"Gagal memuat data: {e}")
        return

    # 2. MLFLOW TRACKING
    with mlflow.start_run():
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("model_type", "XGBoost")

        # Inisiasi dan Latih Model
        model = XGBClassifier(
            n_estimators=n_estimators, 
            learning_rate=learning_rate, 
            max_depth=max_depth, 
            random_state=42,
            eval_metric='logloss'
        )
        model.fit(X_train, y_train)

        # Prediksi dan Evaluasi
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        # LOGGING METRIK
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("f1_score", f1)

        print(f"Hasil -> Accuracy: {acc:.4f} | F1-Score: {f1:.4f}")

        # LOGGING MODEL
        mlflow.xgboost.log_model(model, "xgboost_flight_model")

if __name__ == "__main__":
    DATASET_PATH = "data/processed/tiketcom_20260402_feat.csv" 
    
    print("="*50)
    print("MEMULAI EKSEKUSI 3 VARIASI EKSPERIMEN MLFLOW")
    print("="*50)

    eksperimen_variasi = [
        {"n_estimators": 50, "learning_rate": 0.1, "max_depth": 3},   # Run 1: Ringan
        {"n_estimators": 100, "learning_rate": 0.05, "max_depth": 5}, # Run 2: Sedang
        {"n_estimators": 200, "learning_rate": 0.01, "max_depth": 7}  # Run 3: Kompleks
    ]

    for params in eksperimen_variasi:
        train_model(
            data_path=DATASET_PATH,
            n_estimators=params["n_estimators"],
            learning_rate=params["learning_rate"],
            max_depth=params["max_depth"]
        )
    
    print("\n Pelatihan selesai! Jalankan 'mlflow ui' di terminal untuk melihat hasilnya.")