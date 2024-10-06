-- Sales Analysis

-- Total revenue, Total cost, dan Total profit dari penjualan.
WITH MonthlySales AS (
    SELECT 
        o.order_id,
        o.order_date,      
        oi.subtotal,
        p.cogs,
        oi.quantity         
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
)
SELECT
    EXTRACT(MONTH FROM order_date) AS month, 
    COUNT(DISTINCT order_id) AS number_of_sales,
    SUM(subtotal) AS total_revenue,
    SUM(quantity * cogs) AS total_cost,  
    SUM(subtotal) - SUM(quantity * cogs) AS total_profit 
FROM MonthlySales
GROUP BY 
    month
ORDER BY 
    month;

-- Total penjualan berdasarkan jenis promosi
SELECT  
    pr.promotion_name, 
    SUM(oi.subtotal) AS total_sales
FROM 
    promotions pr 
JOIN 
    products p ON pr.product_id = p.product_id 
JOIN 
    order_items oi ON p.product_id = oi.product_id 
JOIN 
    orders o ON oi.order_id = o.order_id 
WHERE 
    o.order_date BETWEEN pr.start_date AND pr.end_date 
GROUP BY 
    pr.promotion_name;

-- Total penjualan sebelum dan setelah diskon
WITH total_sales AS (
    SELECT 
        o.order_id,
        SUM(oi.subtotal) AS total_sales_before_discount, 
        COALESCE(SUM(oi.quantity * p.price), 0) AS gross_amount, 
        COALESCE(SUM(oi.quantity * p.price * (pr.discount_percentage / 100)), 0) AS discount_amount 
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN promotions pr ON p.product_id = pr.product_id
    GROUP BY o.order_id
)
SELECT 
    ROUND(SUM(ts.gross_amount), 2) AS total_sales_before_discount,  
    ROUND(SUM(ts.discount_amount), 2) AS total_discount,              
    ROUND(SUM(ts.gross_amount) - SUM(ts.discount_amount), 2) AS total_sales_after_discount 
FROM total_sales ts;


--Product Analysis

-- Produk terlaris setiap bulannya
WITH monthly_sales_products AS (
    SELECT 
        EXTRACT(MONTH FROM o.order_date) AS month,
        p.product_name,
        SUM(oi.quantity) AS total_quantity_sold
    FROM 
        order_items oi
    JOIN 
        orders o ON oi.order_id = o.order_id
    JOIN 
        products p ON oi.product_id = p.product_id
    GROUP BY 
        month, p.product_name
),
sales_rank AS (
    SELECT 
        month,
        product_name,
        total_quantity_sold,
        RANK() OVER (PARTITION BY month ORDER BY total_quantity_sold DESC) AS rank
    FROM 
        monthly_sales_products
)
SELECT 
    month,
    product_name,
    total_quantity_sold
FROM 
    sales_rank
WHERE 
    rank = 1
ORDER BY 
    month;

-- TOP 5 Product dengan penjualan tertinggi
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.subtotal) AS total_sales
FROM
    order_items oi
JOIN
    products p ON oi.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY 
    total_sales DESC
LIMIT 5;

-- TOP 5 Product dengan penjualan terendah
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.subtotal) AS total_sales
FROM
    order_items oi
JOIN
    products p ON oi.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY 
    total_sales ASC
LIMIT 5;

--Top 5 Product dengan rata-rata ulasan tertinggi
SELECT 
    p.product_name, 
    ROUND(CAST(AVG(f.rating) AS numeric), 2) AS average_rating
FROM 
    feedbacks f
JOIN 
    products p ON f.product_id = p.product_id
GROUP BY 
    p.product_name
ORDER BY 
    average_rating DESC
LIMIT 5;

--Top 5 Product dengan rata-rata ulasan terendah
SELECT 
    p.product_name, 
    ROUND(CAST(AVG(f.rating) AS numeric), 2) AS average_rating
FROM 
    feedbacks f
JOIN 
    products p ON f.product_id = p.product_id
GROUP BY 
    p.product_name
ORDER BY 
    average_rating ASC
LIMIT 5;

-- Top 10 Product paling banyak diwishlist 
SELECT
   w.product_id, 
    p.product_name,
    COUNT(*) AS wishlist_count 
FROM 
    wishlists w 
JOIN 
    products p ON w.product_id = p.product_id  
GROUP BY 
    w.product_id, p.product_name  
ORDER BY 
    wishlist_count DESC 
LIMIT 10;

-- Produk yang paling banyak dimasukkan ke keranjang
SELECT 
    p.product_id,
    p.product_name,
    COUNT(c.product_id) AS total_added_to_cart
FROM 
    carts c
JOIN 
    products p ON c.product_id = p.product_id
GROUP BY 
    p.product_id, p.product_name
ORDER BY 
    total_added_to_cart DESC
LIMIT 10;

-- Customer Analysis

-- Frekuensi pembelian customer
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    c.email,
    c.phone,
    COUNT(o.order_id) AS purchase_frequency 
FROM 
    customers c
JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, c.email, c.phone
ORDER BY 
    purchase_frequency DESC; 
	
--Customer yang menyimpan wishlist
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    p.product_id, 
    p.product_name, 
    w.created_at,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY w.created_at DESC) AS wishlist_order
FROM 
    wishlists w
JOIN 
    customers c ON w.customer_id = c.customer_id
JOIN 
    products p ON w.product_id = p.product_id
ORDER BY 
    c.customer_id, w.created_at DESC;

--Customer yang memasukkan barang ke keranjang
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    p.product_id,
    p.product_name,
    ct.quantity_cart AS quantity_added
FROM 
    carts ct
JOIN 
    customers c ON ct.customer_id = c.customer_id
JOIN 
    products p ON ct.product_id = p.product_id
ORDER BY 
    c.customer_id, p.product_id;

--Customer yang tidak pernah membeli
SELECT 
    c.customer_id AS customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.phone
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
WHERE 
    o.order_id IS NULL;

-- Total Customer berdasarkan gender
SELECT 
    gender, 
    COUNT(*) AS total_customers
FROM 
    customers
GROUP BY 
    gender;

-- Customer dengan pembelian kurang dari 3x
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.phone,
    COUNT(o.order_id) AS total_orders
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
WHERE 
    o.order_date >= NOW() - INTERVAL '1 year' 
GROUP BY 
    c.customer_id
HAVING 
    COUNT(o.order_id) < 3 
ORDER BY 
    total_orders ASC;

-- Metode Shipping Terbanyak
SELECT 
    shipping_method,
    COUNT(*) AS shipping_count
FROM 
    shipping
GROUP BY 
    shipping_method
ORDER BY 
    shipping_count DESC;

--Metode Pembayaran Terbanyak
SELECT 
    payment_method,
    COUNT(*) AS payment_count
FROM 
    payments
GROUP BY 
    payment_method
ORDER BY 
    payment_count DESC;

--Shipping status
SELECT 
    s.shipping_status, 
    COUNT(*) AS order_count 
FROM 
    shipping s 
GROUP BY 
    s.shipping_status;
