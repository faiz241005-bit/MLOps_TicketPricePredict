# MLOps-FlightPricePrediction

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Proyek ini bertujuan membangun sistem prediksi harga tiket pesawat yang membantu pengguna memutuskan apakah harus membeli sekarang atau menunggu harga lebih murah.

## Project Organization

```text
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── .devcontainer      <- Enviroment Configuration for GitHub Codespace
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         Muhamad Faiz Al Akbar and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes Muhamad Faiz Al Akbar a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations               
```

--------
## Cara Menjalankan di Codespaces

1. Buka halaman repositori GitHub proyek ini.
2. Klik tombol **Code**.
3. Pilih tab **Codespaces**.
4. Klik **Create Codespace on main**.
5. Tunggu hingga lingkungan pengembangan selesai dibuat.

Setelah Codespaces aktif, semua *dependency* akan terinstal secara otomatis dan proyek siap digunakan.

*Nama:* Muhamad Fa'iz Al Akbar  
*NIM:* 235150201111010  
*Mata Kuliah:* Machine Learning Operations (Kelas B)
--------

## Cara Menjalankan Pipeline Data

### 1. Ingestion Data
Mengambil data terbaru dan menyimpan ke `data/raw/`:
```bash
python src/data/ingest_data.py
```

### 2. Preprocessing Data
Membersihkan data dan membuat fitur, output ke `data/processed/`:
```bash
python src/data/preprocess.py
```

### 3. Pelatihan Model (Training)
Melatih model dengan tracking eksperimen MLflow:
```bash
python src/modeling/train.py
```

--------

## Manajemen Versi Data (DVC)

Proyek ini menggunakan **DVC (Data Version Control)** dengan Google Drive sebagai *remote storage* untuk mengelola dataset secara efisien.

**Alur Kerja DVC:**
1. Ingest data harian baru ke `data/raw/`.
2. Lacak perubahan dengan: `dvc add data/raw/[nama_file].csv`.
3. Audit silsilah versi dengan: `dvc diff HEAD~1`.
4. Unggah data fisik ke cloud: `dvc push`.

--------

## Manajemen Eksperimen & Model Metadata (MLflow)

Proyek ini mengintegrasikan **MLflow** untuk manajemen eksperimen dan pelacakan model. Setiap iterasi pelatihan dicatat untuk membandingkan pengaruh *hyperparameter* terhadap performa model.

### Dokumentasi Parameter Terbaik (Best Model for Deployment)

Berdasarkan hasil eksperimen *hyperparameter tuning* menggunakan algoritma **XGBoost Classifier**, berikut adalah metadata model terbaik yang dipilih untuk tahap *deployment* berikutnya:

| Parameter | Nilai Terbaik |
| :--- | :--- |
| **Algorithm** | XGBoost Classifier |
| **n_estimators** | 100 |
| **learning_rate** | 0.05 |
| **max_depth** | 5 |

**Metrik Performa:**
* **Accuracy:** ~0.88
* **F1-Score:** ~0.86

**Ringkasan Analisis:**
Model dengan 100 estimator (`n_estimators`) dan *learning rate* 0.05 dipilih karena memberikan keseimbangan optimal antara akurasi dan generalisasi. Penambahan jumlah estimator hingga 200 terdeteksi menyebabkan *overfitting*, ditandai dengan penurunan metrik pada data uji. Artefak model ini (file `.xgb` dan metadata `MLmodel`) telah terekam secara otomatis di dalam direktori `mlruns/` dan siap untuk tahap *serving*.

--------