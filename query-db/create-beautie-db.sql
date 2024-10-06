-- Table untuk menyimpan data kategori
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    main_category VARCHAR(255) NOT NULL,
    sub_category VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table untuk menyimpan data produk
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    cogs DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    description TEXT,
    product_image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table untuk menyimpan data pelanggan
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20), 
    address TEXT,
    gender VARCHAR(10),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table untuk menyimpan data order
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) ON DELETE CASCADE,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),  
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table untuk menyimpan data order item
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- Table untuk menyimpan data pembayaran
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    payment_date TIMESTAMP NOT NULL,
    payment_method VARCHAR(50), 
    payment_amount DECIMAL(10, 2) NOT NULL
);

-- Table untuk menyimpan data pengiriman
CREATE TABLE shipping (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    shipping_method VARCHAR(50),  
    shipping_cost DECIMAL(10, 2) NOT NULL,
    shipping_status VARCHAR(50),  
    shipped_date TIMESTAMP,
    estimated_delivery TIMESTAMP
);

-- Table untuk menyimpan data feedback
CREATE TABLE feedbacks (
    feedback_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),  
    customer_id INT REFERENCES customers(id),  
    rating FLOAT,
    skin_types VARCHAR(20),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel untuk menyimpan carts
CREATE TABLE carts (
    cart_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

-- Table untuk menyimpan data wishlist
CREATE TABLE wishlists (
    wishlist_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id INT REFERENCES products(id),  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table untuk menyimpan data promosi
CREATE TABLE promotions (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100),
    product_id INT REFERENCES products(id),
    discount_percentage DECIMAL(5, 2),
    start_date DATE,
    end_date DATE
);
