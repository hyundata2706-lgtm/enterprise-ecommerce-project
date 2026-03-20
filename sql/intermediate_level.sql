-- 6 Tính tổng số lượng sản phẩm đã bán (quantity) theo từng category, chỉ lấy các category có tổng > 500
SELECT 
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    COUNT(DISTINCT oi.order_id) AS number_of_orders,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    ROUND(AVG(oi.unit_price), 2) AS avg_selling_price
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id  -- INNER JOIN vì chỉ lấy sản phẩm đã bán
GROUP BY p.category
HAVING SUM(oi.quantity) > 500
ORDER BY total_quantity_sold DESC;
-- 7 Liệt kê users đã mua hàng nhưng chưa từng viết bất kì review nào
SELECT DISTINCT
    u.user_id,
    u.email,
    u.country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    MAX(o.order_date) AS last_order_date
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id  -- Users có orders
WHERE o.status = 'completed'  -- Chỉ orders hoàn thành mới có thể review
  AND NOT EXISTS (  -- Không tồn tại review nào
      SELECT 1 
      FROM reviews r 
      WHERE r.user_id = u.user_id
  )
GROUP BY u.user_id, u.email, u.country
ORDER BY total_orders DESC;
-- 8 Tìm top 3 sản phẩm có doanh thu cao nhất ( dựa trên quantity * unit_price)
SELECT TOP 3
    oi.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    SUM(oi.quantity) AS total_quantity_sold,
    COUNT(DISTINCT oi.order_id) AS number_of_orders
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
-- 9. Tỉ lệ thanh toán thành công (payment_status='success') theo từng payment_method
SELECT payment_method, CAST(CAST(success_time AS DECIMAL(10,2))/total_time AS DECIMAL(10,2)) AS success_rate FROM (
	SELECT 
		payment_method,
		COUNT(payment_id) AS total_time,
		SUM(
		CASE WHEN payment_status = 'success' THEN 1
			 ELSE 0
		END ) AS success_time
	FROM payments
	GROUP BY payment_method
)t 
-- 10 Tìm user đầu tiên (theo registration_date) và user gần nhất theo last_login của mỗi country
WITH user_rankings AS (
    SELECT 
        user_id,
        email,
        country,
        registration_date,
        last_login,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY registration_date ASC) AS rn_earliest,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY last_login DESC) AS rn_latest
    FROM users
)
SELECT 
    country,
    MAX(CASE WHEN rn_earliest = 1 THEN user_id END) AS earliest_user_id,
    MAX(CASE WHEN rn_earliest = 1 THEN email END) AS earliest_user_email,
    MAX(CASE WHEN rn_earliest = 1 THEN registration_date END) AS earliest_registration,
    MAX(CASE WHEN rn_latest = 1 THEN user_id END) AS latest_user_id,
    MAX(CASE WHEN rn_latest = 1 THEN email END) AS latest_user_email,
    MAX(CASE WHEN rn_latest = 1 THEN last_login END) AS latest_login
FROM user_rankings
WHERE rn_earliest = 1 OR rn_latest = 1
GROUP BY country
ORDER BY country;
