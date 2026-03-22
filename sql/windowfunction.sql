-- DAY 1
SELECT user_id, order_date FROM (
	SELECT 
		user_id, 
		order_date,
		ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY order_date DESC) AS rn
	FROM orders
)t WHERE rn=1
-- DAY 2
WITH base AS (
	SELECT 
		order_id, 
		SUM(quantity * unit_price) AS revenue 
	FROM order_items
	GROUP BY order_id
),
e AS (
	SELECT	
		b.order_id,
		b.revenue,
		o.user_id
	FROM base AS b
	INNER JOIN orders AS o
	ON b.order_id = o.order_id
)
SELECT user_id, revenue
FROM (
	SELECT 
		*,
		DENSE_RANK() OVER(
			PARTITION BY user_id 
			ORDER BY revenue DESC
		) AS rn
	FROM e
)t 
WHERE rn <= 3;
-- DAY 3
SELECT 
	user_id, 
	order_date,
	next_order_date,
	DATEDIFF(
		DAY,
		order_date,
		next_order_date
	) AS next_order_day
FROM (
	SELECT 
		user_id, 
		order_date,
		LEAD(order_date) OVER(
			PARTITION BY user_id 
			ORDER BY order_date
		) AS next_order_date
	FROM orders 
)t
-- DAY 4
WITH base AS (
	SELECT 
		user_id, 
		order_date,
		LEAD(order_date) OVER(
			PARTITION BY user_id 
			ORDER BY order_date
		) AS next_order_date
	FROM orders 
),
t AS (
	SELECT 
		user_id,
		DATEDIFF(DAY, order_date, next_order_date) AS next_order_day
	FROM base
	WHERE next_order_date IS NOT NULL
)
SELECT 
	user_id,
	AVG(CAST(next_order_day AS FLOAT)) AS average_days
FROM t
GROUP BY user_id;
-- DAY 6 : MINI PROJECT
WITH m AS (
	SELECT DISTINCT 
		user_id, 
		MIN(order_date) AS min_month
	FROM orders
	GROUP BY user_id
), t AS (
	SELECT 
		user_id,
		DATEFROMPARTS(YEAR(min_month),MONTH(min_month), DAY(min_month)) AS cohort_month
	FROM m
), r AS (
	SELECT
		user_id, 
		DATEFROMPARTS(YEAR(order_date), MONTH(order_date),DAY(order_date)) AS order_date,
		total_amount
	FROM orders
	WHERE status = 'completed'
), j AS (
	SELECT 
		r.user_id,
		r.total_amount,
		r.order_date,
		t.cohort_month
	FROM r AS r
	INNER JOIN
	t AS t
	ON r.user_id = t.user_id
)
SELECT COUNT(DISTINCT user_id) AS total_customers,total_month FROM (
	SELECT
		user_id,
		cohort_month,
		DATEDIFF(MONTH, cohort_month, order_date) AS total_month
	FROM j
)t GROUP BY total_month
