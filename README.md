# Dispenduk-NLP: Hybrid Topic Modeling Analysis

### Analisis Opini Publik Layanan Dispenduk Capil Surabaya menggunakan Pendekatan Hybrid (LDA dan BERTopic)

## 1. Pendahuluan
Proyek ini bertujuan untuk mengeksplorasi pola opini masyarakat terhadap kualitas layanan Dinas Kependudukan dan Pencatatan Sipil (Dispenduk Capil) Kota Surabaya melalui berbagai kanal digital. Menggunakan pendekatan **Unsupervised Machine Learning**, analisis ini berfokus pada eksplorasi isu-isu makro dan mikro tanpa adanya asumsi awal atau pelabelan manual terhadap data (exploratory research).

## 2. Dataset
Data yang dianalisis berjumlah **2.974 dokumen opini** yang dikumpulkan melalui teknik web scraping pada Mei 2026 dari tiga sumber utama:
* **Instagram:** 1.217 data (Komentar pada postingan akun resmi).
* **Google Maps:** 1.650 data (Ulasan lokasi pelayanan dan Siola).
* **Play Store:** 107 data (Ulasan aplikasi Klampid).

## 3. Metodologi: Pendekatan Hybrid
Analisis ini menerapkan arsitektur Hybrid NLP untuk mendapatkan informasi yang komprehensif melalui dua langkah pemodelan:

* **Latent Dirichlet Allocation (LDA) - Macro Approach:** Digunakan untuk memetakan domain masalah utama dalam skala besar. Model ini berhasil mengidentifikasi 3 kategori utama: Prosedur Administrasi, Efektivitas Komunikasi, dan Kualitas Layanan Tatap Muka.
* **BERTopic - Micro Approach:** Memanfaatkan Sentence Embeddings (MiniLM L12 v2) untuk mengekstraksi topik yang lebih granular dan teknis. Model ini mengidentifikasi 6 topik spesifik termasuk masalah verifikasi akun aplikasi, prosedur penggantian foto KTP, hingga pemutakhiran biodata di lokasi pelayanan tertentu.

## 5. Temuan Utama (Key Insights)

* **Sentimen Positif pada Layanan Fisik:** Terdapat apresiasi yang konsisten terhadap keramahan petugas dan kecepatan layanan di lokasi tatap muka, khususnya pada Sentra Pelayanan Joyoboyo dan wilayah Pakal.
* **Hambatan Digital:** Titik kritis pelayanan ditemukan pada proses verifikasi akun aplikasi dan respon pada kanal komunikasi digital (WhatsApp dan Call Center).
* **Validasi Korelasi:** Berdasarkan matriks korelasi, ditemukan hubungan kuat (0.50) antara domain makro layanan fisik dengan klaster mikro apresiasi petugas, yang memvalidasi bahwa kinerja staf lapangan menjadi penggerak utama kepuasan warga.

## 6. Instalasi dan Penggunaan
1. Lakukan clone pada repositori ini:
   ```bash
   git clone [https://github.com/pawbuilds/dispenduk-nlp-analysis.git]
2. Instalasi library yang dibutuhkan
    pip install -r requirements.txt
3. Jalankan notebook pada direktori notebooks/ untuk melihat alur kerja lengkap dari preprocessing hingga modeling.
