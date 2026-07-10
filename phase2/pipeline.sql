-- Mini Cleaning Task: Handled in PySpark but here assuming clean tables

-- 1. Total order amount for each customer
SELECT c.customer_id, c.name, SUM(o.amount) as total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- 2. Top 3 customers by total spend
SELECT c.customer_id, c.name, SUM(o.amount) as total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC
LIMIT 3;

-- 3. Customers with no orders
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 4. City-wise total revenue
SELECT c.city, SUM(o.amount) as total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city;

-- 5. Average order amount per customer
SELECT c.customer_id, c.name, AVG(o.amount) as avg_order_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- 6. Customers with more than one order
SELECT c.customer_id, c.name, COUNT(o.order_id) as order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1;

-- 7. Sort customers by total spend descending
SELECT c.customer_id, c.name, SUM(o.amount) as total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC;
