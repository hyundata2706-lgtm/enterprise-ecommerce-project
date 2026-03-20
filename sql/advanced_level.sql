-- 11 Tính giá trị trung bình 7 ngày gần nhất của tổng doanh thu theo ngày (rolling average)
DECLARE @start_date DATE
SELECT @start_date = DATEADD(day,-7,MAX(order_date)) FROM orders
SELECT ROUND(SUM(total_amount)/COUNT(order_day),2) AS average_amount FROM (
	SELECT
		order_id,
		user_id,
		status,
		total_amount,
		DATEFROMPARTS(YEAR(order_date), MONTH(order_date),DAY(order_date)) AS order_day
	FROM orders
	WHERE status ='completed' AND order_date > @start_date
)t
-- 12 Xếp hạng sản phẩm theo doanh thu trong từng category ( sử dụng RANK() hoặc DENSE_RANK())
SELECT product_name,SUM(amount) AS total_amount_per_product,category,DENSE_RANK() OVER(PARTITION BY category ORDER BY SUM(amount) DESC) AS ranked FROM (
	SELECT DISTINCT oi.order_id,oi.product_id, oi.quantity*oi.unit_price AS amount, p.product_name,p.category 
	FROM order_items AS oi 
	INNER JOIN 
	products AS p
	ON oi.product_id = p.product_id 
)t GROUP BY category, product_name
