import pandas as pd
import colorama
from colorama import Fore, Style
from tabulate import tabulate
import os
os.system('cls') ## Use clear jika menggunakan operating system "Linux/MacOS"
import pwinput

colorama.init(autoreset=True)

# Sample Data (Simulated Database)
products = [
    {
        "UniqueID": 1,
        "Nama Produk": "Susu UHT 1L",
        "Harga Produk": 25000,
        "Stok": 500,
        "Kategori": "Minuman"
    },
    {
        "UniqueID": 2,
        "Nama Produk": "Deterjen Bubuk 1kg",
        "Harga Produk": 35000,
        "Stok": 300,
        "Kategori": "Household"
    },
    {
        "UniqueID": 3,
        "Nama Produk": "Mie Instan Rasa Ayam",
        "Harga Produk": 3500,
        "Stok": 2000,
        "Kategori": "Makanan"
    },
    {
        "UniqueID": 4,
        "Nama Produk": "Sabun Cair 500ml",
        "Harga Produk": 18000,
        "Stok": 400,
        "Kategori": "PersonalCare"
    },
    {
        "UniqueID": 5,
        "Nama Produk": "Minyak Goreng 2L",
        "Harga Produk": 40000,
        "Stok": 250,
        "Kategori": "Makanan"
    },
    {
        "UniqueID": 6,
        "Nama Produk": "Pasta Gigi 150g",
        "Harga Produk": 15000,
        "Stok": 350,
        "Kategori": "PersonalCare"
    },
    {
        "UniqueID": 7,
        "Nama Produk": "Kopi Instan 10sachet",
        "Harga Produk": 22000,
        "Stok": 600,
        "Kategori": "Minuman"
    },
    {
        "UniqueID": 8,
        "Nama Produk": "Tisu Basah 50 lembar",
        "Harga Produk": 12000,
        "Stok": 700,
        "Kategori": "Household"
    },
    {
        "UniqueID": 9,
        "Nama Produk": "Shampoo 250ml",
        "Harga Produk": 30000,
        "Stok": 300,
        "Kategori": "PersonalCare"
    },
    {
        "UniqueID": 10,
        "Nama Produk": "Cokelat Batang 100g",
        "Harga Produk": 27000,
        "Stok": 450,
        "Kategori": "Makanan"
    }
]

recycle_bin = []  # Store deleted products
sales_orders = []  # Menyimpan transaksi pembelian
user_roles = {"manager": "approve", "customer": "buy", "staff": "sell", "logistics": "view_shipment"}

THRESHOLD = 30  # Stok Warning

# Role-based Access
current_user_role = None  # Akan diatur saat login

# User Login System
users = {
    "manager": "pass123",
    "customer": "cust123",
    "staff": "staff123",
    "logistics": "logis123"
}

def login():
    global current_user_role
    attempts = 3
    while attempts > 0:
        username = input("Masukkan username: ")
        password = pwinput.pwinput("Masukkan password: ", mask= "*")
        if username in users and users[username] == password:
            current_user_role = username
            print(Fore.GREEN + f"Login berhasil sebagai {current_user_role}!")
            return
        else:
            attempts -= 1
            print(Fore.RED + f"Login gagal! Sisa percobaan: {attempts}")

    # Jika login gagal setelah 3 kali
    print(Fore.RED + "Anda telah gagal login 3 kali. Program akan keluar.")
    exit()

def get_valid_input(prompt, input_type=int, condition=lambda x: x >= 0, error_message="Input tidak valid!"):
    while True:
        try:
            value = input_type(input(prompt).strip())
            if condition(value):
                return value
            else:
                print(Fore.RED + error_message)
        except ValueError:
            print(Fore.RED + "Harap masukkan nilai yang benar!")

def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ["y", "n"]:
            return choice
        else:
            print(Fore.RED + "Input tidak valid! Masukkan 'y' atau 'n'.")

def read_products():
    print("\nFilter berdasarkan kategori? (y/n)")
    filter_choice = get_yes_no('(y/n)').strip().lower()

    if filter_choice == "y":
        categories = list(set(product["Kategori"] for product in products))
        print("Kategori yang tersedia:")
        for index, category in enumerate(categories, 1):
            print(f"{index}. {category}")

        try:
            category_choices = input("Pilih kategori (pisahkan dengan koma, misal: 1,3): ")
            selected_indices = [int(i.strip()) for i in category_choices.split(",") if i.strip().isdigit()]
            
            invalid_indices = [i for i in selected_indices if i < 1 or i > len(categories)]
            valid_indices = [i for i in selected_indices if 1 <= i <= len(categories)]
            
            if invalid_indices:
                print(Fore.RED + f"Angka {', '.join(map(str, invalid_indices))} tidak terdapat dalam indeks." + Style.RESET_ALL)
            
            selected_categories = {categories[i - 1] for i in valid_indices}
            
            if selected_categories:
                filtered_products = [p for p in products if p["Kategori"] in selected_categories]
            else:
                print(Fore.RED + "Kategori tidak valid, menampilkan semua produk.")
                filtered_products = products
        except ValueError:
            print(Fore.RED + "Input harus berupa angka! Menampilkan semua produk.")
            filtered_products = products
    else:
        filtered_products = products

    # Menyesuaikan kolom yang ditampilkan berdasarkan role user
    if current_user_role == "customer":
        display_columns = ["UniqueID", "Nama Produk", "Harga Produk", "Kategori", "Stok"]
    else:
        display_columns = products[0].keys()  # Semua kolom jika bukan customer

    # Tampilkan tabel dengan tabulate
    print("\nDaftar Produk:")
    display_products = [
        {key: (Fore.YELLOW + str(p[key]) + " (Warning: Stok Rendah!)" + Style.RESET_ALL if key == "Stok" and p["Stok"] <= THRESHOLD else p[key]) for key in display_columns}
        for p in filtered_products
    ]
    print(tabulate(display_products, headers="keys", tablefmt="grid"))

def buy_product():
    read_products()
    cart = []
    total_price = 0
    while True:
        product_id = int(get_valid_input("Masukkan ID produk yang dibeli (0 untuk selesai): "))
        if product_id == 0:
            break
        for product in products:
            if product["UniqueID"] == product_id:
                quantity = int(get_valid_input("Masukkan jumlah yang dibeli: "))
                if quantity > product["Stok"]:
                    print(Fore.RED + "Stok tidak mencukupi!")
                    continue
                product["Stok"] -= quantity
                cart.append({
                    "Nama Produk": product["Nama Produk"], 
                    "Jumlah": quantity, 
                    "Harga Satuan": product["Harga Produk"], 
                    "Total": product["Harga Produk"] * quantity
                })
                total_price += product["Harga Produk"] * quantity
                print(Fore.GREEN + "Produk ditambahkan ke keranjang!")
                break
        else:
            print(Fore.RED + "Produk tidak ditemukan!")

    if cart:
        print("\nKeranjang Belanja:")
        print(tabulate(cart, headers="keys", tablefmt="grid"))
        print(Fore.CYAN + f"Total Belanja: Rp {total_price:,}")

        while True:
            try:
                uang = int(get_valid_input("Tolong masukkan jumlah uang anda: "))
                if uang < total_price:
                    print(Fore.RED + f"Maaf, uang anda kurang sebesar Rp {total_price - uang:,}")
                else:
                    kembalian = uang - total_price
                    if kembalian > 0:
                        print(Fore.GREEN + f"Terima kasih, kembalian Anda sebesar Rp {kembalian:,}")
                    else:
                        print(Fore.GREEN + "Terima kasih, pembayaran pas!")
                    
                    # Status approval (Pending jika di atas 1 juta)
                    approval_status = "Pending" if total_price >= 1000000 else "Approved"
                    pending = 'Pending'
                    
                    # Simpan transaksi ke dalam sales_orders dengan produk yang dibeli
                    sales_orders.append({
                        "ID Order": len(sales_orders) + 1,
                        "Nama Customer": current_user_role,
                        "Total Harga": total_price,
                        "Produk Dibeli": cart,  # Simpan produk yang dibeli
                        "Approval Status": approval_status,
                        "Shipment Status": pending
                    })

                    print(Fore.GREEN + "Pembayaran berhasil! Terima kasih telah berbelanja.")
                    print(Fore.LIGHTYELLOW_EX + "Apakah anda ingin receipt? (y/n)")
                    export = get_yes_no("(y/n)").strip().lower()

                    if export == 'y':
                        export_receipt(cart, total_price, uang, kembalian)

                    break 
                    
                    
            except ValueError:
                print(Fore.RED + "Masukkan jumlah uang yang valid!")

def approve_sales():
    pending_orders = [order for order in sales_orders if order["Approval Status"] == "Pending"]
    
    if not pending_orders:
        print(Fore.YELLOW + "Tidak ada transaksi yang perlu diapprove.")
        return

    print("\nTransaksi yang menunggu approval:")
    for order in pending_orders:
        print(Fore.CYAN + f"\nID Order: {order['ID Order']}")
        print(f"Nama Customer: {order['Nama Customer']}")
        print(f"Total Harga: Rp {order['Total Harga']:,}")
        print("Produk Dibeli:")
        print(tabulate(order["Produk Dibeli"], headers="keys", tablefmt="grid"))
        print(f"Approval Status: {order['Approval Status']}")
    
    try:
        approve_id = int(get_valid_input("\nMasukkan ID Order yang ingin diapprove (0 untuk batal): "))
        if approve_id == 0:
            return
        
        order_found = False
        for order in pending_orders:
            if order["ID Order"] == approve_id:
                order["Approval Status"] = "Approved"
                order["Shipment Status"] = "Pending"  # Setelah diapprove, masuk ke logistik  
                print(Fore.GREEN + f"Transaksi ID {approve_id} telah diapprove dan siap untuk dikirim!")
                order_found = True
                break
        
        if not order_found:
            print(Fore.RED + f"ID Order {approve_id} tidak ditemukan!")
    
    except ValueError:
        print(Fore.RED + "Masukkan ID yang valid!")

def approve_shipment():
    approved_orders = [order for order in sales_orders if order["Approval Status"] == "Approved" and order["Shipment Status"] == "Pending"]

    if not approved_orders:
        print(Fore.YELLOW + "Tidak ada transaksi yang perlu dikirim.")
        return

    print("\nTransaksi yang siap untuk dikirim:")
    for order in approved_orders:
        print(Fore.CYAN + f"\nID Order: {order['ID Order']}")
        print(f"Nama Customer: {order['Nama Customer']}")
        print(f"Total Harga: Rp {order['Total Harga']:,}")
        print("Produk Dibeli:")
        print(tabulate(order["Produk Dibeli"], headers="keys", tablefmt="grid"))
        print(f"Shipment Status: {order['Shipment Status']}")

    try:
        shipment_id = int(get_valid_input("\nMasukkan ID Order yang telah dikirim (0 untuk batal): "))
        if shipment_id == 0:
            return
        
        order_found = False
        for order in approved_orders:
            if order["ID Order"] == shipment_id:
                order["Shipment Status"] = "Delivered"
                print(Fore.GREEN + f"Transaksi ID {shipment_id} telah dikirim dan status berubah menjadi 'Delivered'!")
                order_found = True
                break
        
        if not order_found:
            print(Fore.RED + f"ID Order {shipment_id} tidak ditemukan!")
    
    except ValueError:
        print(Fore.RED + "Masukkan ID yang valid!")


def export_receipt(cart, total_price, uang_dibayar, kembalian):
    df = pd.DataFrame(cart)
    df["Total Harga"] = total_price
    df["Uang Dibayar"] = uang_dibayar
    df["Kembalian"] = kembalian

    df.to_excel("receipt.xlsx", index=False)
    print(Fore.GREEN + "Struk pembelian berhasil diekspor ke receipt.xlsx")

def add_product():
    global products
    print("\nTambah Produk Baru:")
    try:
        nama_produk = input("Masukkan Nama Produk: ").strip()
        stok = int(get_valid_input("Masukkan Stok Produk: "))

        if stok <= 0:
            print(Fore.RED + "Stok harus lebih dari 0!")
            return

        existing_product = next((p for p in products if p["Nama Produk"].lower() == nama_produk.lower()), None)
        
        if existing_product:
            existing_product["Stok"] += stok
            print(Fore.GREEN + f"Stok produk {nama_produk} berhasil ditambahkan!")
        else:
            harga_produk = int(get_valid_input("Masukkan Harga Produk: "))
            kategori = input("Masukkan Kategori Produk: ").strip()
            
            if harga_produk <= 0:
                print(Fore.RED + "Harga harus lebih dari 0!")
                return

            unique_id = max([p["UniqueID"] for p in products]) + 1 if products else 1  # Auto-increment UniqueID
            
            new_product = {
                "UniqueID": unique_id,
                "Nama Produk": nama_produk,
                "Harga Produk": harga_produk,
                "Stok": stok,
                "Kategori": kategori,
            }

            products.append(new_product)
            print(Fore.GREEN + f"Produk {nama_produk} berhasil ditambahkan!")
    except ValueError:
        print(Fore.RED + "Input tidak valid! Pastikan stok dan harga adalah angka.")

def sell_product():
    read_products()
    product_id = int(get_valid_input("Masukkan ID produk yang dijual: "))
    for product in products:
        if product["UniqueID"] == product_id:
            quantity = int(get_valid_input("Masukkan jumlah yang dijual: "))
            if quantity > product["Stok"]:
                print(Fore.RED + "Stok tidak mencukupi!")
                return
            product["Stok"] -= quantity
            print(Fore.GREEN + "Penjualan berhasil!")
            return
    print(Fore.RED + "Produk tidak ditemukan!")


def delete_product():
    read_products()
    product_id = int(get_valid_input("Masukkan ID produk yang ingin dihapus: "))
    
    for product in products:
        if product["UniqueID"] == product_id:
            recycle_bin.append(product)  # Pindahkan ke recycle bin
            products.remove(product)  # Hapus dari daftar utama
            print(Fore.YELLOW + f"Produk {product['Nama Produk']} telah dipindahkan ke Recycle Bin.")
            return
    
    print(Fore.RED + "Produk tidak ditemukan!")

def restore_product():
    if not recycle_bin:
        print(Fore.RED + "Recycle Bin kosong.")
        return
    
    print("\nProduk di Recycle Bin:")
    print(tabulate(recycle_bin, headers="keys", tablefmt="grid"))
    
    product_id = int(get_valid_input("Masukkan ID produk yang ingin direstore: "))
    
    for product in recycle_bin:
        if product["UniqueID"] == product_id:
            existing_product = next((p for p in products if p["Nama Produk"].lower() == product["Nama Produk"].lower()), None)
            
            if existing_product:
                existing_product["Stok"] += product["Stok"]
                print(Fore.GREEN + f"Stok produk {product['Nama Produk']} telah ditambahkan kembali.")
            else:
                products.append(product)
                print(Fore.GREEN + f"Produk {product['Nama Produk']} telah dikembalikan.")
            
            recycle_bin.remove(product)
            return
    
    print(Fore.RED + "Produk tidak ditemukan di Recycle Bin.")

def read_sales_orders():
    if not sales_orders:
        print("\nTidak ada data Sales Orders yang tersedia.")
        return

    # Menyesuaikan kolom yang ditampilkan berdasarkan role user
    if current_user_role == "customer":
        display_columns = ["OrderID", "Tanggal Order", "Nama Produk", "Jumlah", "Total Harga", "Status"]
    else:
        display_columns = sales_orders[0].keys()  # Semua kolom jika bukan customer

    # Tampilkan tabel dengan tabulate
    print("\nDaftar Sales Orders:")
    display_orders = [
        {key: order.get(key, "-") for key in display_columns} for order in sales_orders
    ]
    print(tabulate(display_orders, headers="keys", tablefmt="grid"))



def logout():
    global current_user_role
    print(Fore.YELLOW + "Logout berhasil. Kembali ke menu login.")
    current_user_role = None
    main()

def main():
    login()
    while True:
        print("\nMenu:")
        if current_user_role == "customer":
            print("1. Lihat Produk")
            print("2. Beli Produk")
            print("6. Logout")
            print("7. Keluar")
        elif current_user_role == "staff":
            print("1. Lihat Produk")
            print("2. Jual Produk")
            print("3. Tambah Produk")
            print("4. Hapus Produk")
            print("5. Restore Produk")
            print("6. Logout")
            print("7. Keluar")
            
        elif current_user_role == "manager":
            print("1. Lihat Produk")
            print("2. Approve Penjualan")
            print("3. Melihat Transaksi")
            print("6. Logout")
            print("7. Keluar")

        elif current_user_role == "logistics":
            print("1. Lihat Produk")
            print("2. Handling Logistik")
            print("6. Logout")
            print("7. Keluar")
            
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            read_products()
        elif pilihan == "2" and current_user_role == "customer":
            buy_product()
        elif pilihan == "2" and current_user_role == "manager":
            approve_sales()
        elif pilihan == "2" and current_user_role == "logistics":
            approve_shipment()
        elif pilihan == "2" and current_user_role == "staff":
            sell_product()
        elif pilihan == "3" and current_user_role == "staff":
            add_product()
        elif pilihan == "3" and current_user_role == "manager":
            read_sales_orders()
        elif pilihan == "4" and current_user_role == "staff":
            delete_product()
        elif pilihan == "5" and current_user_role == "staff":
            restore_product()
        
        elif pilihan == "6":
            logout()
        elif pilihan == "7":
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")

if __name__ == "__main__":
    main()
