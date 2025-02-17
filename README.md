# Capstone_Module1
# Inventory Trade Management System

## Deskripsi

### Inventory Management System ini adalah aplikasi berbasis Python yang digunakan untuk mengelola stok produk, melakukan transaksi penjualan, serta mengelola persetujuan transaksi dan pengiriman. Aplikasi ini dirancang dengan fitur berbasis peran (role-based access) sehingga hanya pengguna tertentu yang dapat melakukan tindakan tertentu.

## Fitur Utama

### 1. Sistem Login Berbasis Peran

     Role Access:

- Manager: Dapat menyetujui transaksi dan melihat transaksi.

- Customer: Dapat membeli produk.

- Staff: Dapat menjual dan menambah produk.

- Logistics: Dapat mengatur status pengiriman.

### Manajemen Produk

- Melihat daftar produk dengan filter berdasarkan kategori.

- Menambah produk baru ke dalam sistem.

- Menghapus produk dari sistem dengan fitur pemulihan (recycle bin).

- Transaksi Pembelian

- Customer dapat memilih produk dan menambahkannya ke keranjang.

- Sistem secara otomatis memeriksa stok yang tersedia.

- Jika total harga transaksi melebihi batas tertentu, persetujuan manager diperlukan.

- Fitur ekspor struk pembelian ke file Excel.

- Persetujuan Transaksi dan Pengiriman

- Logistics dapat mengubah status pengiriman setelah transaksi disetujui.

- Sistem akan memberikan peringatan jika stok suatu produk mendekati ambang batas yang ditentukan.


### Instalasi dan Penggunaan

1. Instalasi Dependensi

    Sebelum menjalankan aplikasi, pastikan Python dan pustaka berikut sudah terinstal:

    " pip install pandas colorama tabulate pwinput openpyxl "

2. Menjalankan Program

    Jalankan script dengan perintah berikut:

    python Capstone_Module1.py

3. Login

    Gunakan salah satu akun berikut untuk login:

- (Role): (Username) / (Password)

- Manager: manager / pass123

- Customer: customer / cust123

- Staff: staff / staff123

- Logistics: logistics / logis123

4. Navigasi dalam Program

- Melihat Produk: Pilih opsi untuk melihat daftar produk.

- Menambah Produk: Hanya staff yang dapat menambah produk.

- Membeli Produk: Customer dapat memilih produk dan membayarnya.

- Menyetujui Transaksi: Hanya manager yang dapat menyetujui transaksi.

- Mengatur Pengiriman: Hanya logistics yang dapat mengubah status pengiriman.

## Flowchart
## Main Menu

![alt text](<Flowchart Main Menu.png>)  

## Struktur Data

### 1. products

### Berisi daftar produk yang tersimpan dalam bentuk list of dictionaries:

    products = [
    {
        "UniqueID": 1,
        "Nama Produk": "Susu UHT 1L",
        "Harga Produk": 25000,
        "Stok": 500,
        "Kategori": "Minuman",
    }
]

### 2. sales_orders

### Menyimpan data transaksi yang telah dilakukan:

    sales_orders = [
    {
        "ID Order": 1,
        "Nama Customer": "customer",
        "Total Harga": 50000,
        "Produk Dibeli": [{"Nama Produk": "Susu UHT 1L", "Jumlah": 2}],
        "Approval Status": "Pending",
        "Shipment Status": "Pending"
    }
]

## Fitur Keamanan

- Sistem login menggunakan pwinput untuk menyembunyikan input password.

- Batas percobaan login maksimal 3 kali sebelum keluar otomatis.


## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan bebas digunakan serta dimodifikasi.


