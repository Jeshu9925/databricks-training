-- Assuming tables `customers` and `sales` exist

-- 1. Calculate daily sales
SELECT order_date, SUM(amount) as daily_sales
FROM sales
WHERE amount IS NOT NULL
GROUP BY order_date
ORDER BY order_date;

-- 2. City-wise revenue
SELECT c.city, SUM(s.amount) as city_revenue
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
WHERE c.age > 0 AND c.age IS NOT NULL
GROUP BY c.city
ORDER BY city_revenue DESC;

-- 3. Find repeat customers (>2 orders)
SELECT customer_id, COUNT(order_id) as order_count
FROM sales
GROUP BY customer_id
HAVING COUNT(order_id) > 2;

-- 4. Find highest spending customer in each city
WITH CustomerSpend AS (
    SELECT c.city, c.name, SUM(s.amount) as total_spend
    FROM customers c
    JOIN sales s ON c.customer_id = s.customer_id
    WHERE c.age > 0 AND c.age IS NOT NULL
    GROUP BY c.city, c.name
),
RankedSpend AS (
    SELECT city, name, total_spend,
           RANK() OVER(PARTITION BY city ORDER BY total_spend DESC) as rnk
    FROM CustomerSpend
)
SELECT city, name, total_spend
FROM RankedSpend
WHERE rnk = 1;

-- 5. Build final reporting table with customer, city, total spend, order count
SELECT 
    c.customer_id,
    c.name,
    c.city,
    SUM(s.amount) as total_spend,
    COUNT(s.order_id) as order_count
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
WHERE c.age > 0 AND c.age IS NOT NULL
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spend DESC;
