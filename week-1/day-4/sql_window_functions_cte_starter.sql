
-- SQL Window Functions and CTE Assignment
-- Compatible with PostgreSQL

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(100),
    manager_id INT NULL,
    salary DECIMAL(10,2),
    hire_date DATE
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    employee_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Insert Employees
INSERT INTO employees VALUES
(1, 'Alice Johnson', 'Sales', NULL, 70000, '2020-01-15'),
(2, 'Bob Smith', 'Sales', 1, 65000, '2021-03-20'),
(3, 'Charlie Brown', 'IT', NULL, 90000, '2019-07-01'),
(4, 'Diana Prince', 'IT', 3, 95000, '2018-11-11'),
(5, 'Ethan Hunt', 'HR', NULL, 60000, '2022-02-10'),
(6, 'Fiona Green', 'HR', 5, 58000, '2023-05-12'),
(7, 'George Miller', 'Finance', NULL, 85000, '2017-09-18'),
(8, 'Hannah Lee', 'Finance', 7, 82000, '2021-08-30');

-- Insert Customers
INSERT INTO customers VALUES
(1, 'Acme Corp', 'New York'),
(2, 'Tech Solutions', 'Chicago'),
(3, 'Global Retail', 'Dallas'),
(4, 'Blue Sky Ltd', 'Seattle'),
(5, 'NextGen Systems', 'Boston');

-- Insert Orders
INSERT INTO orders VALUES
(101, 1, 1, '2024-01-10', 500),
(102, 2, 2, '2024-01-11', 700),
(103, 1, 1, '2024-01-15', 1200),
(104, 3, 3, '2024-01-18', 300),
(105, 4, 4, '2024-01-20', 900),
(106, 5, 2, '2024-01-25', 1500),
(107, 2, 1, '2024-02-01', 650),
(108, 1, 3, '2024-02-05', 1100),
(109, 3, 4, '2024-02-10', 400),
(110, 4, 2, '2024-02-15', 950),
(111, 5, 1, '2024-02-20', 2000),
(112, 1, 4, '2024-02-25', 750);

-- Notes:
-- Multiple departments for PARTITION BY exercises.
-- Salary variations for ranking exercises.
-- Multiple customer orders for LAG/LEAD analysis.
-- Manager hierarchy included for recursive CTE practice.
