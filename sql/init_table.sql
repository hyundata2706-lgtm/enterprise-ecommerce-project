CREATE DATABASE ENTERPRISEECOMMERCE
USE ENTERPRISEECOMMERCE

DROP TABLE IF EXISTS payments, order_items, reviews, orders, products, users;

CREATE TABLE users(
	user_id INT PRIMARY KEY,
	email NVARCHAR(50) ,
	country NVARCHAR(50),
	registration_date NVARCHAR(50),
	last_login NVARCHAR(50), 
	is_active NVARCHAR(10)
)
CREATE TABLE products(
	product_id INT PRIMARY KEY,
	product_name NVARCHAR(MAX),
	category NVARCHAR(50),
	brand NVARCHAR(50),
	price DECIMAL(10,2),
	stock_quantity INT, 
	created_at NVARCHAR(50)
)

CREATE TABLE orders(
	order_id INT PRIMARY KEY,
	user_id INT,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	order_date NVARCHAR(50),
	status NVARCHAR(50),
	total_amount FLOAT
)

CREATE TABLE order_items(
	order_item_id INT PRIMARY KEY,
	order_id INT,
	FOREIGN KEY (order_id) REFERENCES orders(order_id),
	product_id INT,
	FOREIGN KEY (product_id) REFERENCES products(product_id),
	quantity INT,
	unit_price FLOAT
)

CREATE TABLE reviews (
	review_id INT PRIMARY KEY,
	user_id INT,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	product_id INT,
	FOREIGN KEY (product_id) REFERENCES products(product_id),
	Rating INT, 
	review_text NVARCHAR(MAX),
	created_at NVARCHAR(50)
)

CREATE TABLE payments(
	payment_id INT PRIMARY KEY,
	order_id INT,
	FOREIGN KEY (order_id) REFERENCES orders(order_id),
	payment_method NVARCHAR(50),
	payment_status NVARCHAR(50),
	amount DECIMAL(18,2),
	payment_date NVARCHAR(50)
)
