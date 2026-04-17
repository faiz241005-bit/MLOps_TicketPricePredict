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

### 3. Jalankan Keduanya Sekaligus
```bash
python src/data/ingest_data.py && python src/data/preprocess.py
```

--------

## Manajemen Versi Data & Continual Learning (DVC)

Proyek ini menerapkan *Continuous Training* untuk beradaptasi dengan fluktuasi harga tiket pesawat yang sangat dinamis. Agar repositori Git tetap ringan dan tidak terbebani file biner berukuran besar, pengelolaan dan pelacakan versi dataset dilakukan menggunakan **DVC (Data Version Control)** yang terintegrasi dengan Google Drive sebagai *remote storage*.

Berikut adalah alur kerja untuk menyimulasikan masuknya data harian baru dan melacak transisi versinya (Sesuai dengan LK-05):

### 1. Ingesti Data Baru (Simulasi Continual Learning)
Jalankan skrip ingestion untuk menarik sekumpulan data harga tiket terbaru. Sistem akan mendeteksi dan menambahkan data (append) ke dalam folder `data/raw/`.
```bash
python src/data/ingest_data.py
```

### 2. Pelacakan Data Baru (Versioning)
Gunakan DVC untuk melacak file dataset yang baru saja diperbarui. DVC akan menghitung *hash value* baru untuk mencatat versi spesifik dari data tersebut.
```bash
dvc add data/raw/tiketcom_YYYYMMDD.csv
```

### 3. Audit dan Diff Metadata
Lakukan pengecekan silsilah perubahan data untuk memverifikasi bahwa DVC mengenali adanya ukuran file atau entitas baru yang ditambahkan dibandingkan versi sebelumnya.
```bash
dvc diff HEAD~1
```

### 4. Simpan Riwayat ke Git
File dataset fisik dikelola oleh DVC, sementara file metadata/penunjuk (`.dvc`) disimpan ke dalam Git agar riwayat versi data selalu sinkron dengan versi kode (*codebase*).
```bash
git add data/raw/tiketcom_YYYYMMDD.csv.dvc
git commit -m "track: penambahan data batch harian untuk continual learning"
```

### 5. Unggah ke Remote Storage
Dorong data fisik asli dengan aman ke Google Drive untuk menghemat kapasitas ruang kerja lokal.
```bash
dvc push
```