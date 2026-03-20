# enterprise-ecommerce-project

1. build 1 project với python , sql để thực hiện những câu lệnh truy vấn từ cơ bản đến nâng cao trong SQL
2. Database Schema: Gồm 4 Schema
  a. users
    Column	Type	Description
    user_id	INT	PK
    email	VARCHAR	Unique
    country	VARCHAR	
    registration_date	DATE	
    last_login	TIMESTAMP	
    is_active	BOOLEAN
  b. products
    Column	Type	Description
    product_id	INT	PK
    product_name	VARCHAR	
    category	VARCHAR	
    brand	VARCHAR	
    price	DECIMAL(10,2)	
    stock_quantity	INT	
    created_at	DATE
  c. orders
    Column	Type	Description
    order_id	INT	PK
    user_id	INT	FK to users
    order_date	TIMESTAMP	
    status	VARCHAR	(completed, cancelled, pending)
    total_amount	DECIMAL(10,2)
  d. order_items
    Column	Type	Description
    order_item_id	INT	PK
    order_id	INT	FK to orders
    product_id	INT	FK to products
    quantity	INT	
    unit_price	DECIMAL(10,2)
  f. reviews
    Column	Type	Description
    review_id	INT	PK
    user_id	INT	FK to users
    product_id	INT	FK to products
    rating	INT	1–5
    review_text	TEXT	
    created_at	TIMESTAMP
  g. payments
    Column	Type	Description
    payment_id	INT	PK
    order_id	INT	FK to orders
    payment_method	VARCHAR	(credit_card, paypal, bank_transfer)
    payment_status	VARCHAR	(success, failed, pending)
    amount	DECIMAL(10,2)	
    payment_date	TIMESTAMP
3. Data volume
  Mỗi bảng sẽ có ≥ 1,000 rows:
  users: 5,000 rows
  products: 2,000 rows
  orders: 10,000 rows
  order_items: 30,000 rows
  reviews: 8,000 rows
  payments: 9,000 rows
4. Mục tiêu của dự án
   a. ETL Simulation: Sinh dữ liệu Python, insert vào DB, đảm bảo data integrity
   b. SQL mastery:  viết và tối ưu các câu query từ cơ bản đến phức tạp
   c. sử dụng EXPLAIN ANALYZE , tạo indexes hợp lí
   d. viết queries phát hiện null, duplicate, outliers
