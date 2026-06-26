# MindBalance Dashboard

> Analisis & Prediksi Tingkat Stres serta Rekomendasi Gaya Hidup

Dashboard interaktif berbasis **Streamlit** untuk mengeksplorasi hubungan antara gaya hidup digital dan kesehatan mental, dilengkapi simulasi prediksi tingkat stres personal.

---

## Deskripsi Proyek

MindBalance menganalisis dataset 3.000 responden dari 7 negara untuk memahami bagaimana kebiasaan sehari-hari — seperti jam tidur, screen time, olahraga, dan pola makan — berkaitan dengan kondisi mental dan tingkat kebahagiaan.

**Tema:** Healthy Lives & Well-being  
**ID Tim:** CC26 - PSU281

---

## Struktur File

```
├── Dashboard.py              # Main Streamlit application
├── Mental_Health_Cleaned.xlsx# Dataset utama (3.000 responden)
├── url                       # URL deployment aplikasi
├── requirements              # Daftar dependensi
├── Logo.png                  # Logo aplikasi
├── Pattern.png               # Background pattern
└── README.md
```

---

## Dataset

| Atribut | Detail |
|---|---|
| Jumlah Responden | 3.000 |
| Jumlah Negara | 7 |
| Jumlah Variabel | 12 |

**Variabel yang tersedia:**

| Variabel | Tipe |
|---|---|
| Age | Numerik |
| Gender | Kategori |
| Country | Kategori |
| Exercise Level | Kategori |
| Diet Type | Kategori |
| Sleep Hours | Numerik |
| Stress Level | Kategori |
| Mental Health Condition | Kategori |
| Work Hours per Week | Numerik |
| Screen Time per Day (Hours) | Numerik |
| Social Interaction Score | Numerik |
| Happiness Score | Numerik |

---

## Cara Menjalankan

### 1. Siapkan Proyek

Pastikan semua file berikut berada dalam satu folder yang sama:
- `Dashboard.py`
- `Mental_Health_Cleaned.xlsx`
- `Logo.png`
- `Pattern.png`
- `requirements`

### 2. Install dependensi

```bash
pip install -r requirements
```

### 3. Jalankan aplikasi

```bash
streamlit run Dashboard.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

---

## 📦 Requirements

```
numpy==2.4.6
pandas==3.0.3
plotly==6.5.0
streamlit==1.41.0
```

---

## 🗺️ Halaman & Fitur

### 🏠 Beranda
- KPI utama: total responden, jumlah negara, kondisi mental, variabel
- Distribusi kondisi mental (donut chart)
- Distribusi responden per negara
- 6 insight utama yang dihitung otomatis dari data

### 📈 Analisis Data (EDA)
Filter dinamis berdasarkan: negara, kondisi mental, tingkat stres, gender, dan rentang usia.

Terdiri dari 4 tab:

| Tab | Konten |
|---|---|
| **Demografi & Target** | Distribusi usia, stres, gender, dan negara |
| **Gaya Hidup** | Tidur vs stres, screen time vs happiness, olahraga, jam kerja, diet |
| **Kondisi Mental** | Distribusi kondisi, happiness score, jam tidur, screen time per kondisi |
| **Korelasi** | Heatmap korelasi, scatter plot, ranking variabel vs happiness |

### 🔮 Simulasi Prediksi
Input gaya hidup personal untuk mendapatkan:
- Estimasi tingkat stres (Low / Moderate / High)
- Estimasi Happiness Score (skala 1–10)
- Rekomendasi personal berbasis input
- Radar chart profil gaya hidup vs kondisi ideal
- Kesimpulan analisis dengan area kuat & area yang perlu ditingkatkan

---

## 🎯 Pertanyaan Bisnis (BQ)

| BQ | Pertanyaan |
|---|---|
| BQ 1 | Distribusi stres & kondisi mental |
| BQ 2 | Durasi tidur vs tingkat stres |
| BQ 3 | Olahraga vs happiness score |
| BQ 4 | Variabel numerik vs stres |
| BQ 5 | Pola harian per kondisi mental |
| BQ 6 | Diet vs happiness score |

---

## 🎨 Desain

- **Warna utama:** Palet hijau natural (`#3A8C5C`, `#4CAF7D`, `#F0FAF4`)
- **Font:** DM Sans + DM Mono (Google Fonts)
- **Library visualisasi:** Plotly (bar, pie, scatter, box, violin, heatmap, radar)

---

## ⚠️ Disclaimer

Simulasi prediksi bersifat **indikatif** berdasarkan pola heuristik dari data 3.000 responden. Hasil ini bukan diagnosis medis. Konsultasikan dengan profesional kesehatan untuk evaluasi lebih lanjut.

---

## 👥 Tim

Proyek ini dikembangkan sebagai bagian dari Capstone Project dengan tema **Healthy Lives & Well-being**.
