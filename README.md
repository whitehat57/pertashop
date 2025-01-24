# Sistem Manajemen Pertashop 🏪

Aplikasi manajemen untuk Pertashop dengan fitur pencatatan stok, penjualan, dan laporan keuangan.

## Fitur 📋

- Dashboard stok BBM realtime
- Pencatatan penjualan BBM
- Laporan penjualan dengan filter tanggal
- Manajemen stok BBM
- Pengaturan harga jual dan beli
- Notifikasi stok minimum
- Format mata uang Rupiah
- Penyimpanan data ke CSV

## Persyaratan Sistem 💻

- Python 3.7 atau lebih baru
- pip (Python package installer)

## Instalasi 🔧

1. Clone repository ini atau download source code
```bash
git clone https://github.com/whitehat57/pertashop.git
cd pertashop
```

2. Buat virtual environment (opsional tapi direkomendasikan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Locale (opsional, untuk format mata uang)
```bash
# Windows
# Tidak perlu setup khusus, akan menggunakan system locale

# Linux/Ubuntu
sudo apt-get update
sudo apt-get install language-pack-id
```

## Penggunaan 🚀

1. Jalankan program
```bash
python pertashop.py
```

2. Menu yang tersedia:
   - Tampilkan Dashboard Stok BBM
   - Catat Penjualan BBM
   - Tampilkan Laporan Penjualan
   - Tambah Stok BBM
   - Ubah Harga BBM

## Struktur Data 📁

Program akan membuat dua file CSV untuk menyimpan data:
- `stok_bbm.csv`: Menyimpan data stok dan harga BBM
- `penjualan.csv`: Menyimpan riwayat transaksi penjualan

## Troubleshooting ⚠️

1. Error locale setting:
   - Program akan otomatis menggunakan fallback ke format default
   - Tidak mempengaruhi fungsionalitas program

2. File CSV tidak terbaca:
   - Pastikan file memiliki permission yang benar
   - Program akan membuat file baru dengan data default jika file tidak ditemukan

## Kontribusi 🤝

Silakan buat issue atau pull request jika ingin berkontribusi pada pengembangan program ini.

## Lisensi 📄

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan. 
