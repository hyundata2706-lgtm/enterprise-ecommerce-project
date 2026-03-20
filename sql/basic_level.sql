-- FILTERING
-- AGGREGATION
-- SORTING

-- 1 Liệt kê tất cả users active ở Việt Nam, sắp xếp theo ngày đăng ký mới nhất.
SELECT * 
FROM users 
WHERE country = 'Vietnam' AND is_active = 'TRUE' 
ORDER BY last_login DESC
-- 2 Tính tổng số orders theo từng status
SELECT 
	status, 
	COUNT(order_id) AS total_orders 
FROM orders 
GROUP BY status
-- 3 Top 5 sản phẩm có giá cao nhất
SELECT TOP 5 *
FROM products 
ORDER BY price DESC
-- 4 Đếm số lượng reviews theo từng rating
SELECT 
	Rating, 
	COUNT(review_id) AS total_reviews 
FROM reviews 
GROUP BY Rating
-- 5 Tính tổng doanh thu (total_amount) từ các orders có status='completed'
SELECT SUM(total_amount) AS total_amount 
FROM orders 
WHERE status = 'completed'





