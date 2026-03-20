
BULK INSERT users
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\users.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)

BULK INSERT products
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\products.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)

BULK INSERT orders
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\orders.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)

BULK INSERT order_items
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\order_items.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)


BULK INSERT reviews
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\reviews.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROloadWTERMINATOR = '\n'
)


BULK INSERT payments
FROM 'C:\Users\ADMIN\PycharmProjects\enterprise-ecommerce-project\ecommerce_data_generator\data\payments.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
