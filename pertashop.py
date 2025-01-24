import csv
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
import locale

# Set locale untuk format mata uang
try:
    # Coba set locale ke Indonesia
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        # Fallback ke en_US jika id_ID tidak tersedia
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        # Fallback ke default system locale jika keduanya tidak tersedia
        locale.setlocale(locale.LC_ALL, '')

# Inisialisasi konsol Rich
console = Console()

# Nama file untuk menyimpan data
STOK_FILE = 'stok_bbm.csv'
PENJUALAN_FILE = 'penjualan.csv'

# Data stok BBM default
DEFAULT_STOK_BBM = {
    'Pertamax': {
        'stok_awal': 5000,
        'harga_beli': 9000,
        'harga_jual': 10000,
        'stok_minimum': 1000
    },
    'Pertalite': {
        'stok_awal': 7000,
        'harga_beli': 7000,
        'harga_jual': 7500,
        'stok_minimum': 1500
    }
}

def format_rupiah(amount):
    try:
        # Coba gunakan currency format dari locale
        return locale.currency(amount, grouping=True, symbol=True)
    except locale.Error:
        # Fallback ke format manual jika gagal
        return f"Rp {amount:,.0f}".replace(',', '.')

def load_stok_data():
    if not os.path.exists(STOK_FILE):
        return DEFAULT_STOK_BBM
    
    try:
        stok_bbm = {}
        with open(STOK_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stok_bbm[row['jenis']] = {
                    'stok_awal': float(row['stok_awal']),
                    'harga_beli': int(row['harga_beli']),
                    'harga_jual': int(row['harga_jual']),
                    'stok_minimum': float(row['stok_minimum'])
                }
        return stok_bbm
    except Exception as e:
        console.print(f"Error loading stok data: {e}", style="bold red")
        return DEFAULT_STOK_BBM

def save_stok_data(stok_bbm):
    try:
        with open(STOK_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['jenis', 'stok_awal', 'harga_beli', 'harga_jual', 'stok_minimum'])
            writer.writeheader()
            for jenis, data in stok_bbm.items():
                writer.writerow({
                    'jenis': jenis,
                    'stok_awal': data['stok_awal'],
                    'harga_beli': data['harga_beli'],
                    'harga_jual': data['harga_jual'],
                    'stok_minimum': data['stok_minimum']
                })
    except Exception as e:
        console.print(f"Error saving stok data: {e}", style="bold red")

def load_penjualan():
    penjualan = []
    if os.path.exists(PENJUALAN_FILE):
        try:
            with open(PENJUALAN_FILE, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['jumlah_liter'] = float(row['jumlah_liter'])
                    row['pendapatan'] = float(row['pendapatan'])
                    row['keuntungan'] = float(row['keuntungan'])
                    penjualan.append(row)
        except Exception as e:
            console.print(f"Error loading penjualan data: {e}", style="bold red")
    return penjualan

# Data stok BBM dan penjualan
stok_bbm = load_stok_data()
penjualan = load_penjualan()

def simpan_data_penjualan(data_penjualan):
    try:
        with open(PENJUALAN_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['tanggal', 'jenis', 'jumlah_liter', 'pendapatan', 'keuntungan'])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data_penjualan)
    except IOError as e:
        console.print(f"Gagal menyimpan data penjualan: {e}", style="bold red")

def tampilkan_dashboard():
    table = Table(title="\U0001F4CA Dashboard Stok Pertashop")

    table.add_column("Jenis BBM", justify="left", style="cyan")
    table.add_column("Stok Tersedia (Liter)", justify="right", style="green")
    table.add_column("Harga Beli", justify="right", style="yellow")
    table.add_column("Harga Jual", justify="right", style="magenta")
    table.add_column("Status Stok", justify="center", style="bold")

    for jenis, data in stok_bbm.items():
        status = "🟢 Normal"
        if data['stok_awal'] <= data['stok_minimum']:
            status = "🔴 Kritis"
        elif data['stok_awal'] <= data['stok_minimum'] * 1.5:
            status = "🟡 Menipis"
            
        table.add_row(
            jenis,
            f"{data['stok_awal']:,.2f}",
            format_rupiah(data['harga_beli']),
            format_rupiah(data['harga_jual']),
            status
        )

    console.print(table)

def tambah_stok():
    console.rule("\U0001F69C Tambah Stok BBM")
    jenis = Prompt.ask("Masukkan jenis BBM", choices=list(stok_bbm.keys()))
    
    try:
        jumlah = float(Prompt.ask("Masukkan jumlah liter yang ditambahkan"))
        if jumlah <= 0:
            console.print("Jumlah harus lebih dari 0!", style="bold red")
            return
            
        stok_bbm[jenis]['stok_awal'] += jumlah
        save_stok_data(stok_bbm)
        console.print(f"✅ Berhasil menambah {jumlah:,.2f} liter {jenis}", style="bold green")
    except ValueError:
        console.print("Input tidak valid!", style="bold red")

def catat_penjualan():
    console.rule("\U0001F4B0 Mencatat Penjualan")
    jenis = Prompt.ask("Pilih jenis BBM", choices=list(stok_bbm.keys()))

    try:
        jumlah_liter = float(Prompt.ask("Masukkan jumlah liter"))
        if jumlah_liter <= 0:
            console.print("Jumlah harus lebih dari 0!", style="bold red")
            return
            
        if jumlah_liter > stok_bbm[jenis]['stok_awal']:
            console.print("Stok BBM tidak mencukupi!", style="bold red")
            return

        # Konfirmasi penjualan
        total_harga = jumlah_liter * stok_bbm[jenis]['harga_jual']
        console.print(Panel(f"""
Detail Penjualan:
Jenis BBM: {jenis}
Jumlah: {jumlah_liter:,.2f} liter
Total Harga: {format_rupiah(total_harga)}
        """))
        
        if not Confirm.ask("Konfirmasi penjualan?"):
            return

        pendapatan = jumlah_liter * stok_bbm[jenis]['harga_jual']
        biaya = jumlah_liter * stok_bbm[jenis]['harga_beli']
        keuntungan = pendapatan - biaya

        # Update stok
        stok_bbm[jenis]['stok_awal'] -= jumlah_liter
        save_stok_data(stok_bbm)

        # Simpan data penjualan
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_penjualan = {
            'tanggal': tanggal,
            'jenis': jenis,
            'jumlah_liter': jumlah_liter,
            'pendapatan': pendapatan,
            'keuntungan': keuntungan
        }
        penjualan.append(data_penjualan)
        simpan_data_penjualan(data_penjualan)

        console.print(f"✅ Penjualan {jenis} sebanyak {jumlah_liter:,.2f} liter berhasil dicatat!", style="bold green")
        
        # Notifikasi restock
        cek_stock_minimum(jenis)
        
    except ValueError:
        console.print("Input tidak valid!", style="bold red")

def tampilkan_laporan_penjualan():
    if not penjualan:
        console.print("Belum ada penjualan yang dicatat.", style="yellow")
        return

    # Filter berdasarkan tanggal
    tgl_mulai = Prompt.ask("Masukkan tanggal mulai (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
    tgl_akhir = Prompt.ask("Masukkan tanggal akhir (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))

    filtered_penjualan = [
        p for p in penjualan 
        if tgl_mulai <= p['tanggal'].split()[0] <= tgl_akhir
    ]

    if not filtered_penjualan:
        console.print("Tidak ada data penjualan untuk periode tersebut.", style="yellow")
        return

    table = Table(title=f"\U0001F4DC Laporan Penjualan ({tgl_mulai} s/d {tgl_akhir})")

    table.add_column("Tanggal", justify="left", style="cyan")
    table.add_column("Jenis BBM", justify="left", style="cyan")
    table.add_column("Jumlah Liter", justify="right", style="green")
    table.add_column("Pendapatan", justify="right", style="magenta")
    table.add_column("Keuntungan", justify="right", style="yellow")

    total_pendapatan = 0
    total_keuntungan = 0
    total_liter = {}

    for data in filtered_penjualan:
        table.add_row(
            data['tanggal'],
            data['jenis'],
            f"{data['jumlah_liter']:,.2f}",
            format_rupiah(data['pendapatan']),
            format_rupiah(data['keuntungan'])
        )
        total_pendapatan += data['pendapatan']
        total_keuntungan += data['keuntungan']
        
        # Hitung total liter per jenis
        if data['jenis'] not in total_liter:
            total_liter[data['jenis']] = 0
        total_liter[data['jenis']] += data['jumlah_liter']

    # Menambahkan baris total
    table.add_row(
        "TOTAL", 
        "", 
        "", 
        format_rupiah(total_pendapatan),
        format_rupiah(total_keuntungan),
        style="bold"
    )

    console.print(table)
    
    # Tampilkan ringkasan per jenis BBM
    console.print("\n📊 Ringkasan per Jenis BBM:", style="bold cyan")
    for jenis, total in total_liter.items():
        console.print(f"{jenis}: {total:,.2f} liter")

def cek_stock_minimum(jenis):
    if stok_bbm[jenis]['stok_awal'] < stok_bbm[jenis]['stok_minimum']:
        console.print(Panel(
            f"⚠️  PERINGATAN: Stok {jenis} sudah di bawah batas minimum!\n" +
            f"Stok saat ini: {stok_bbm[jenis]['stok_awal']:,.2f} liter\n" +
            f"Batas minimum: {stok_bbm[jenis]['stok_minimum']:,.2f} liter\n" +
            "Silakan lakukan restock segera!",
            style="bold red"
        ))

def ubah_harga():
    console.rule("💵 Ubah Harga BBM")
    jenis = Prompt.ask("Pilih jenis BBM", choices=list(stok_bbm.keys()))
    
    console.print(f"\nHarga {jenis} saat ini:")
    console.print(f"Harga Beli: {format_rupiah(stok_bbm[jenis]['harga_beli'])}")
    console.print(f"Harga Jual: {format_rupiah(stok_bbm[jenis]['harga_jual'])}")
    
    try:
        # Input harga baru
        harga_beli_baru = int(Prompt.ask("\nMasukkan harga beli baru (kosongkan jika tidak berubah)", 
                                        default=str(stok_bbm[jenis]['harga_beli'])))
        harga_jual_baru = int(Prompt.ask("Masukkan harga jual baru (kosongkan jika tidak berubah)", 
                                        default=str(stok_bbm[jenis]['harga_jual'])))
        
        # Validasi harga
        if harga_jual_baru < harga_beli_baru:
            console.print("⚠️ Peringatan: Harga jual lebih rendah dari harga beli!", style="bold yellow")
            if not Confirm.ask("Apakah Anda yakin ingin melanjutkan?"):
                return
        
        # Konfirmasi perubahan
        console.print(Panel(f"""
Detail Perubahan Harga {jenis}:
Harga Beli: {format_rupiah(stok_bbm[jenis]['harga_beli'])} → {format_rupiah(harga_beli_baru)}
Harga Jual: {format_rupiah(stok_bbm[jenis]['harga_jual'])} → {format_rupiah(harga_jual_baru)}
Margin: {format_rupiah(stok_bbm[jenis]['harga_jual'] - stok_bbm[jenis]['harga_beli'])} → {format_rupiah(harga_jual_baru - harga_beli_baru)}
        """))
        
        if Confirm.ask("Konfirmasi perubahan harga?"):
            # Update harga
            stok_bbm[jenis]['harga_beli'] = harga_beli_baru
            stok_bbm[jenis]['harga_jual'] = harga_jual_baru
            save_stok_data(stok_bbm)
            console.print(f"✅ Harga {jenis} berhasil diperbarui!", style="bold green")
            
    except ValueError:
        console.print("Input tidak valid! Harga harus berupa angka.", style="bold red")

def main():
    console.print(Panel.fit(
        "🏪 Selamat datang di Sistem Manajemen Pertashop",
        style="bold cyan"
    ))
    
    while True:
        console.rule("📋 Menu Utama")
        console.print("""
1. 📊 Tampilkan Dashboard Stok BBM
2. 💰 Catat Penjualan BBM
3. 📈 Tampilkan Laporan Penjualan
4. 🚛 Tambah Stok BBM
5. 💵 Ubah Harga BBM
6. ❌ Keluar
        """)
        
        pilihan = Prompt.ask("Pilih menu", choices=['1', '2', '3', '4', '5', '6'])

        if pilihan == '1':
            tampilkan_dashboard()
        elif pilihan == '2':
            catat_penjualan()
        elif pilihan == '3':
            tampilkan_laporan_penjualan()
        elif pilihan == '4':
            tambah_stok()
        elif pilihan == '5':
            ubah_harga()
        elif pilihan == '6':
            console.print("👋 Terima kasih telah menggunakan sistem ini. Sampai jumpa!", style="bold green")
            break

if __name__ == "__main__":
    main()
