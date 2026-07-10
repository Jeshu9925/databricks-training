-- Phase 4: SQL Business Pipeline & Analytics

-- Assuming raw tables `raw_customers` and `raw_sales` exist.
-- First, we define cleaned temporary views/tables as requested:
-- Data Cleaning:
--   - Remove rows with null keys (customer_id etc.)
--   - Remove duplicate rows
--   - Filter invalid values (negative amounts)

CREATE OR REPLACE TEMP VIEW clean_customers AS
SELECT DISTINCT 
    CAST(customer_id AS INT) as customer_id,
    name,
    city
FROM raw_customers
WHERE customer_id IS NOT NULL;

CREATE OR REPLACE TEMP VIEW clean_sales AS
SELECT DISTINCT
    CAST(order_id AS INT) as order_id,
    CAST(customer_id AS INT) as customer_id,
    CAST(amount AS DOUBLE) as amount,
    order_date
FROM raw_sales
WHERE customer_id IS NOT NULL 
  AND order_id IS NOT NULL
  AND CAST(amount AS DOUBLE) > 0;


-- Task 1: Daily Sales → Output: date, total_sales
SELECT 
    order_date AS date, 
    SUM(amount) AS total_sales
FROM clean_sales
GROUP BY order_date
ORDER BY date;


-- Task 2: City-wise Revenue → Output: city, total_revenue
SELECT 
    c.city, 
    SUM(s.amount) AS total_revenue
FROM clean_sales s
JOIN clean_customers c ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;


-- Task 3: Top 5 Customers → Output: customer_name, total_spend
SELECT 
    c.name AS customer_name, 
    SUM(s.amount) AS total_spend
FROM clean_sales s
JOIN clean_customers c ON s.customer_id = c.customer_id
GROUP BY c.name
ORDER BY total_spend DESC
LIMIT 5;


-- Task 4: Repeat Customers (>1 order) → Output: customer_id, order_count
SELECT 
    customer_id, 
    COUNT(order_id) AS order_count
FROM clean_sales
GROUP BY customer_id
HAVING COUNT(order_id) > 1
ORDER BY order_count DESC;


-- Task 5: Customer Segmentation → total_spend > 10000 → Gold, 5000–10000 → Silver, <5000 → Bronze
-- Output: customer_name, total_spend, segment
WITH CustomerSpend AS (
    SELECT 
        c.name AS customer_name, 
        SUM(s.amount) AS total_spend
    FROM clean_sales s
    JOIN clean_customers c ON s.customer_id = c.customer_id
    GROUP BY c.name
)
SELECT 
    customer_name, 
    total_spend,
    CASE 
        WHEN total_spend > 10000 THEN 'Gold'
        WHEN total_spend >= 5000 AND total_spend <= 10000 THEN 'Silver'
        ELSE 'Bronze'
    END AS segment
FROM CustomerSpend
ORDER BY total_spend DESC;


-- Task 6: Final Reporting Table
-- Output should include: customer_name, city, total_spend, order_count, segment
WITH CustomerSummary AS (
    SELECT 
        c.name AS customer_name, 
        c.city,
        SUM(s.amount) AS total_spend,
        COUNT(s.order_id) AS order_count
    FROM clean_sales s
    JOIN clean_customers c ON s.customer_id = c.customer_id
    GROUP BY c.name, c.city
)
SELECT 
    customer_name, 
    city, 
    total_spend, 
    order_count,
    CASE 
        WHEN total_spend > 10000 THEN 'Gold'
        WHEN total_spend >= 5000 AND total_spend <= 10000 THEN 'Silver'
        ELSE 'Bronze'
    END AS segment
FROM CustomerSummary
ORDER BY total_spend DESC;
