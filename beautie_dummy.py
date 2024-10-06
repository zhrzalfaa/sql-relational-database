from faker import Faker
import random
import psycopg2
import os
from datetime import timedelta
from dotenv import load_dotenv
import pandas as pd

# Load .env file
load_dotenv()

# Initialize Faker
faker = Faker()

# Database connection
conn = None
try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    print("Koneksi ke database berhasil!")

    with conn.cursor() as cursor:
        # Fungsi untuk menghasilkan data categories
        def data_categories(num_categories=1000): # Jumlah kolom yang diinginkan
            categories = [] # Daftar untuk menyimpan data category
            category_list = {  # Daftar kategori utama dan sub-kategori
                "Skincare": ["Facial Wash", "Toner", "Serum", "Moisturizer", "Sunscreen"],
                "Makeup": ["Powder", "Foundation", "Blush On", "Lipstick", "Mascara", "Eyebrow"]
            } 
           # Menghasilkan kategori produk
            for _ in range(num_categories): 
                main_category = random.choice(list(category_list.keys())) # Memilih kategori utama secara acak dari daftar kategori
                sub_category = random.choice(category_list[main_category]) # Memilih sub-kategori secara acak dari kategori utama
                description = faker.sentence()   # Menghasilkan deskripsi kategori secara acak
                # Menambahkan data category
                categories.append((main_category, sub_category, description)) #
            return categories

        # Insert data categories ke database
        def insert_categories(cursor, categories):
            sql = "INSERT INTO categories (main_category, sub_category, description) VALUES (%s, %s, %s)"
            cursor.executemany(sql, categories)  # Eksekusi perintah SQL untuk table kategori
            conn.commit()

        # Fungsi untuk menghasilkan data products
        def data_products(categories, num_products=1000):  
            products = [] # Daftar untuk menyimpan data product
            product_names = {  # Daftar nama produk
                "Facial Wash": ["COSRX FW", "Hadalabo Facial Wash", "Skintific Fw", "Somethinc Facial Wash", "Avoskin Facial Wash"],
                "Toner": ["COSRX Retinol Toner", "Hadalabo Hydra Toner", "Skintific Toner", "Somethinc Hydra Toner", "Avoskin Exfo Toner"],
                "Serum": ["COSRX Exfo Serum", "Hadalabo Retinol Serum", "Skintific Hydra Serum", "Somethinc Serum", "Avoskin Exfo Serum"],
                "Moisturizer": ["COSRX Gel Moist", "Hadalabo Moisturizer", "Skintific Cream Moist", "Somethinc Calm Down", "Avoskin Moist"],
                "Sunscreen": ["COSRX 35 PA++", "Hadalabo 50++ PA", "Skintific 45 PA+", "Somethinc 50 PA+++", "Avoskin 30 PA++"],
                "Powder": ["Wardah Powder", "Makeover Loose Powder", "Emina Loose PowderW", "Focallure Compact Powder", "Implora Compact Powder"],
                "Foundation": ["Wardah Liquid Foundation", "Makeover Foundation", "Emina Cream Foundation", "Focallure Balm Foundation", "Implora Liquid Foundation"],
                "Blush On": ["Wardah Powder Blush", "Makeover Liquid Blush", "Emina Liquid Blush", "Focallure Powder Blush", "Implora Powder Blush"],
                "Lipstick": ["Wardah Liptint", "Makeover Lip Stay", "Emina Lipcream", "Focallure Lipbalm", "Implora Lipstick"],
                "Mascara": ["Wardah Mascara", "Makeover Mascara", "Emina Mascara", "Focallure Mascara", "Implora Mascara"]
            }
            # Menghasilkan data produk
            for _ in range(num_products):
                sub_category = random.choice(list(product_names.keys())) # Memilih sub-kategori secara acak dari daftar sub-kategori
                product_name = random.choice(product_names[sub_category]) # Memilih nama produk secara acak dari sub-kategori yang dipilih
                # Menentukan kategori utama berdasarkan sub-kategori yang dipilih
                main_category = "Skincare" if sub_category in ["Facial Wash", "Toner", "Serum", "Moisturizer", "Sunscreen"] else "Makeup"
                # Memastikan category_id berada di kategori yang benar
                category_id = next((index + 1 for index, (mc, sc, _) in enumerate(categories)
                            if mc == main_category and sc == sub_category), None)
                if category_id is not None:
                    cogs = round(random.uniform(50000, 200000), 1)  # Menghasilkan COGS secara acak dalam rentang 50.000 hingga 200.000
                    price = round(cogs * 1.2, 1)  # Menghitung harga jual dengan menambahkan 20% dari COGS
                    stock_quantity = random.randint(10, 500)  # Menghasilkan jumlah stok secara acak antara 10 hingga 500
                    description = faker.sentence() # Menghasilkan deskripsi produk secara acak menggunakan Faker
                    product_image_url = faker.image_url() # Menghasilkan URL gambar produk secara acak menggunakan Faker
                    # Menambahkan data product
                    products.append((product_name, category_id, cogs, price, stock_quantity, description, product_image_url))
            return products

        # Insert data products ke database 
        def insert_products(cursor, products):
            sql = "INSERT INTO products (product_name, category_id, cogs, price,  stock_quantity, description, product_image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, products) # Eksekusi perintah SQL untuk table produk
            conn.commit()

        # Fungsi untuk menghasilkan data customers
        def data_customers(num_customers=1000):  
            customers = [] # Daftar untuk menyimpan data customer
            email_set = set()  # Set untuk menyimpan email yang unik
            while len(customers) < num_customers: 
                first_name = faker.first_name()  # Menghasilkan nama depan secara acak
                last_name = faker.last_name() # Menghasilkan nama belakang secara acak
                email = faker.email() # Menghasilkan email secara acak
                while email in email_set: # Memastikan email yang dihasilkan unik
                    email = faker.email() # Menghasilkan email baru jika sudah ada di set
                email_set.add(email) # Menambahkan email unik ke dalam set
                phone = faker.phone_number()[:10] # Menghasilkan 10 digit nomor telepon
                address = faker.address() # Menghasilkan alamat secara acak
                gender = random.choice(['Male', 'Female']) # Menghasilkan gender secara acak
                city = faker.city() # Menghasilkan nama kota secara acak
                # Menambahkan data customer
                customers.append((first_name, last_name, email, phone, address, gender, city))
            return customers

        # Insert data customers ke database
        def insert_customers(cursor, customers):
            sql = "INSERT INTO customers (first_name, last_name, email, phone, address, gender, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, customers) # Eksekusi perintah SQL untuk table customers
            conn.commit()

        # Fungsi untuk menghasilkan data products
        def data_orders(customers, num_orders=1000):  
            orders = [] # Daftar untuk menyimpan data customer
            for _ in range(num_orders):
                customer_id = random.choice(range(1, len(customers) + 1)) # Memilih secara acak customer_id dari daftar customer yang ada
                order_date = faker.date_time_this_year() # Menghasilkan tanggal dan waktu pesanan yang dibuat dalam tahun ini
                status = random.choice(['Pending', 'Completed', 'Shipped', 'Cancelled']) # Memilih status pesanan secara acak dari daftar yang sudah ditentukan
                total_amount = round(random.uniform(50000, 1000000) * 1.05, 2) # Menghasilkan total jumlah pesanan secara acak antara 50.000 hingga 1.000.000
                shipping_address = faker.address() # Menghasilkan alamat pengiriman secara acak
                 # Menambahkan data orders ke table orders
                orders.append((customer_id, order_date, status, total_amount, shipping_address))
            return orders

        # Insert data orders ke database
        def insert_orders(cursor, orders):
            sql = "INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_address) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, orders) # Eksekusi perintah SQL untuk table orders
            conn.commit()

        # # Fungsi untuk menghasilkan data order_items
        def data_order_items(orders, products, num_items=1000):  
            order_items = [] # Daftar untuk menyimpan data customer
            for _ in range(num_items):
                order_id = random.choice(range(1, len(orders) + 1)) # Memilih secara acak order_id dari daftar order yang ada
                product_id = random.choice(range(1, len(products) + 1)) # Memilih secara acak product_id dari daftar produk yang ada
                quantity = random.randint(1, 10)  # Menghasilkan jumlah item yang dibeli secara acak antara 1 hingga 10
                unit_price = products[product_id - 1][3]  # Mengambil data harga dari table products 
                subtotal = round(unit_price * quantity, 2) # Menghitung subtotal 
                # Menambahkan data item pesanan
                order_items.append((order_id, product_id, quantity, unit_price, subtotal))
            return order_items

        # Insert data order items ke database
        def insert_order_items(cursor, order_items):
            sql = "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, order_items) # Eksekusi perintah SQL untuk table order items
            conn.commit()

        # Fungsi untuk menghasilkan table payments
        def data_payments(orders, num_payments=1000):  
            payments = [] # Daftar untuk menyimpan data customer
            for _ in range(num_payments):
                order_id = random.choice(range(1, len(orders) + 1)) # Memilih secara acak order_id dari daftar order yang ada
                payment_date = faker.date_time_this_year()  # Menghasilkan tanggal pembayaran acak dalam tahun ini
                payment_method = random.choice(['COD', 'Credit Card', 'E-wallet', 'Bank Transfer']) # Memilih metode pembayaran secara acak dari daftar metode yang ditentukan
                payment_amount = next((order[3] for order in orders if order[0] == order_id), 0)  # Mencari jumlah pembayaran berdasarkan order_id, jika tidak ditemukan, gunakan 0 sebagai default
                 # Menambahkan data pembayaran ke daftar payments
                payments.append((order_id, payment_date, payment_method, payment_amount)) 
            return payments

        # Insert data payments ke database
        def insert_payments(cursor, payments):
            sql = "INSERT INTO payments (order_id, payment_date, payment_method, payment_amount) VALUES (%s, %s, %s, %s)"
            cursor.executemany(sql, payments) # Eksekusi perintah SQL untuk table payments
            conn.commit()

        # Fungsi untuk menghasilkan data shipping
        def data_shipping(orders, num_shipping=1000):  
            shipping = [] # Daftar untuk menyimpan data shipping 
            for _ in range(num_shipping):
                order_id = random.choice(range(1, len(orders) + 1)) # Memilih order_id secara acak dari daftar order yang ada
                shipping_method = random.choice(['Standard', 'Express']) # Memilih metode pengiriman secara acak
                shipping_cost = round(random.uniform(5000, 50000), 2) # Menghasilkan biaya pengiriman secara acak antara 5000 dan 50000
                shipping_status = random.choice(['Processing', 'Shipped', 'Delivered', 'Cancelled']) # Memilih status pengiriman secara acak
                shipped_date = faker.date_time_this_year() # Menghasilkan tanggal pengiriman secara acak dalam tahun ini
                 # Menghitung estimasi tanggal pengiriman berdasarkan metode pengiriman
                if shipping_method == 'Standard':
                    estimated_delivery = shipped_date + timedelta(days=random.randint(5, 10))  # 5-10 hari
                else:  # Express
                    estimated_delivery = shipped_date + timedelta(days=random.randint(1, 5))  # 1-5 hari
                # Menambahkan data shipping
                shipping.append((order_id, shipping_method, shipping_cost, shipping_status, shipped_date, estimated_delivery))
            return shipping

        # Insert data shipping ke database
        def insert_shipping(cursor, shipping):
            sql = "INSERT INTO shipping (order_id, shipping_method, shipping_cost, shipping_status, shipped_date, estimated_delivery) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, shipping) # Eksekusi perintah SQL untuk table shipping
            conn.commit()

        # Fungsi untuk menghasilkan data feedbacks
        def data_feedbacks(customers, products, num_reviews=800):  
            reviews = []  # Daftar untuk menyimpan data ulasan
            skin_type_list = ['Dry', 'Oily', 'Normal'] # # Daftar menyimpan jenis kulit

            for _ in range(num_reviews):
                customer_id = random.choice(range(1, len(customers) + 1)) # Memilih customer_id secara acak dari daftar customers yang ada
                product_id = random.choice(range(1, len(products) + 1)) # Memilih order_id secara acak dari daftar orders yang ada
                rating = round(random.uniform(1.0, 5.0), 1)  # Menghasilkan rating secara acak antara 1.0 dan 5.0
                skin_types = random.choice(skin_type_list) # Memilih jenis kulit secara acak dari daftar jenis kulit
                created_at = faker.date_time_this_year() # Menghasilkan tanggal ulasan secara acak dalam tahun ini

                
                review = "" # Variabel untuk menyimpan isi ulasan
                # Menentukan isi ulasan berdasarkan rating yang diberikan
                if rating in [1.0, 2.0, 3.0]: # Jika rating adalah 1.0, 2.0, atau 3.0 berikan ulasan negatif
                        review = random.choice([
                            "The product didn't work well for my skin.",
                            "My skin broke out after using this product.",
                            "Not hydrating enough for my skin.",
                            "The serum caused irritation on my skin.",
                            "This moisturizer made my skin too oily.",
                            "This sunscreen leaves a white cast and feels heavy."
                            "The lipstick dried out my lips.",
                            "The powder left my face looking cakey.",
                            "This foundation didn't blend well.",
                            "The mascara clumped my lashes.",
                            "The eyebrow pencil was too waxy.",
                            "The quality of this makeup product is disappointing."
                            "The shipping was delayed and the package arrived late.",
                            "The package was damaged during delivery."
                        ])
                elif rating > 3.0: # Jika rating bukan 1.0, 2.0, atau 3.0 berikan ulasan positif
                    review = random.choice([
                            "The product is amazing!",
                            "It worked for my skin!",
                            "Highly recommend this product!",
                            "Great value for money!",
                            "Best skincare product I've used!"
                            "The package arrived on time and in perfect condition.",
                            "The shipping very fast."
                            "The lipstick is long-lasting and feels great!",
                            "The powder gives a flawless matte finish.",
                            "This foundation blends beautifully on my skin.",
                            "The mascara makes my lashes look voluminous.",
                            "The eyebrow pencil gives a natural look.",
                            "This makeup product exceeded my expectations."
                            "The package arrived on time and in perfect condition.",
                            "The shipping was fast"
                    ])
                    
                full_review = f"{review}"
                # Menambahkan data feedbacks
                reviews.append((product_id, customer_id, rating, skin_types, review, created_at))

            return reviews

        # Insert data feedbacks ke database
        def insert_feedbacks(cursor, feedbacks):
            sql =  "INSERT INTO feedbacks (product_id, customer_id, rating, skin_types, review, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, feedbacks) # Eksekusi perintah SQL untuk table feedbacks
            conn.commit()

        # Fungsi untuk menyimpan data shopping cart
        def data_cart(customers, products, num_cart=800):
            carts = [] # Daftar untuk menyimpan data cart
            for _ in range(num_cart):
                customer_id = random.choice(range(1, len(customers)+ 1))  # Memilih customer_id secara acak dari daftar customers yang ada
                product_id = random.choice(range(1, len(products)+ 1)) # # Memilih product_id secara acak dari daftar produk yang ada
                quantity_cart = random.randint(1, 10) # Menghasilkan umlah produk dalam keranjang 
                created_at = faker.date_time_this_year()  # Tanggal produk ditambahkan ke cart dalam tahun ini
                # Menambahkan data cart
                carts.append((customer_id, product_id, quantity_cart, created_at))
            return carts
        
        # Insert data cart ke database
        def insert_cart(cursor, carts):
            sql = "INSERT INTO carts (customer_id, product_id, quantity_cart, created_at) VALUES( %s, %s, %s, %s)"
            cursor.executemany(sql, carts) # Eksekusi perintah SQL untuk table carts
            cursor.connection.commit()

        #Fungsi untuk menyimpan data wishlist
        def data_wishlists(customers, products, num_wishlists=500):
            wishlists = [] # Daftar untuk menyimpan data wishlist
            for _ in range(num_wishlists):
                customer_id = random.choice(range(1, len(customers) + 1))  # Memilih customer_id secara acak dari daftar customers yang ada
                product_id = random.choice(range(1, len(products) + 1))   # Memilih product_id secara acak dari daftar produk yang ada
                created_at = faker.date_time_this_year()  # Tanggal produk ditambahkan ke wishlist dalam tahun ini
                # Menambahkan data wishlists 
                wishlists.append((customer_id, product_id, created_at))
            return wishlists

        # Insert data wishlists ke database
        def insert_wishlists(cursor, wishlists):
            sql = "INSERT INTO wishlists (customer_id, product_id, created_at) VALUES (%s, %s, %s)"
            cursor.executemany(sql, wishlists) # Eksekusi perintah SQL untuk table wishlists
            cursor.connection.commit()

        def data_promotions(products, num_promotions=100):
            promotions = [] # Daftar untuk menyimpan data promosi
            promotions_name = [ # Daftar nama promosi 
                 "Free Delivery for All Shipping Methods",
                 "Discount 50% All Products",
                 "Discount 20% Bundle Skincare+Makeup",
                 "Discount 10% for Credit Card",
                 "Discount 5% for All Payment Methods"
            ]
    
            for _ in range(num_promotions):
                promotion_name = random.choice(promotions_name)  # Memilih nama promosi secara acak dari daftar
                product_id = random.choice(range(1, len(products) + 1))  # Memilih product_id secara acak dari daftar produk yang ada
                # Menentukan persentase diskon berdasarkan nama promosi
                discount_percentage = 0  
                if promotion_name == "Discount 50% All Products":
                    discount_percentage = 50.00
                elif promotion_name == "Discount 20% Bundle Skincare+Makeup":
                    discount_percentage = 20.00
                elif promotion_name == "Discount 10% for Credit Card":
                    discount_percentage = 10.00
                elif promotion_name == "Discount 5% for All Payment Methods":
                    discount_percentage = 5.00
                # Menghasilkan tanggal mulai promosi dalam tahun ini
                start_date = faker.date_this_year() 
                end_date = faker.date_between(start_date=start_date, end_date='today')  # Tanggal akhir setelah tanggal mulai
                #M Menambahkan data promotions
                promotions.append((promotion_name, product_id, discount_percentage, start_date, end_date))
                
            return promotions
        
        # Insert data promotions ke database
        def insert_promotions(cursor, promotions):
            sql = "INSERT INTO promotions (promotion_name, product_id, discount_percentage, start_date, end_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, promotions) # Eksekusi perintah SQL untuk table promotions
            cursor.connection.commit()

        # Menjalankan semua fungsi
        categories = data_categories()
        insert_categories(cursor, categories)

        products = data_products(categories)
        insert_products(cursor, products)

        customers = data_customers()
        insert_customers(cursor, customers)

        orders = data_orders(customers)
        insert_orders(cursor, orders)

        order_items = data_order_items(orders, products)
        insert_order_items(cursor, order_items)

        payments = data_payments(orders)
        insert_payments(cursor, payments)

        shipping = data_shipping(orders)
        insert_shipping(cursor, shipping)

        feedbacks = data_feedbacks(customers, products)
        insert_feedbacks(conn.cursor(), feedbacks)

        carts = data_cart(customers, products)
        insert_cart(conn.cursor(), carts)

        wishlists = data_wishlists(customers, products)
        insert_wishlists(conn.cursor(), wishlists)

        promotions = data_promotions(products)
        insert_promotions(conn.cursor(), promotions)

except Exception as e:
    print(f"Error connecting to database: {e}")

finally:
    if conn:
        conn.close()
