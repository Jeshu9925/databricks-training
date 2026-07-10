from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, col

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Phase2_Bridge_Pack") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Load Data
customers = spark.read.option("header", "true").csv("./samples/customers.csv", inferSchema=True)
orders = spark.read.option("header", "true").csv("./samples/orders.csv", inferSchema=True)

print("--- Original Data ---")
customers.show()
orders.show()

# Mini Cleaning Task: Remove rows with missing customer_id
customers = customers.dropna(subset=["customer_id"])
orders = orders.dropna(subset=["customer_id"])

# 1. Total order amount for each customer
print("--- 1. Total order amount for each customer ---")
joined_df = customers.join(orders, "customer_id", "inner")
total_amount_df = joined_df.groupBy("customer_id", "name").agg(sum("amount").alias("total_amount"))
total_amount_df.show()

# 2. Top 3 customers by total spend
print("--- 2. Top 3 customers by total spend ---")
top_3_df = total_amount_df.orderBy(col("total_amount").desc()).limit(3)
top_3_df.show()

# 3. Customers with no orders
print("--- 3. Customers with no orders ---")
no_orders_df = customers.join(orders, "customer_id", "left_anti")
no_orders_df.select("customer_id", "name").show()

# 4. City-wise total revenue
print("--- 4. City-wise total revenue ---")
city_revenue_df = joined_df.groupBy("city").agg(sum("amount").alias("total_revenue"))
city_revenue_df.show()

# 5. Average order amount per customer
print("--- 5. Average order amount per customer ---")
avg_order_df = joined_df.groupBy("customer_id", "name").agg(avg("amount").alias("avg_order_amount"))
avg_order_df.show()

# 6. Customers with more than one order
print("--- 6. Customers with more than one order ---")
multi_order_df = joined_df.groupBy("customer_id", "name").agg(count("order_id").alias("order_count")).filter(col("order_count") > 1)
multi_order_df.show()

# 7. Sort customers by total spend descending
print("--- 7. Sort customers by total spend descending ---")
sorted_spend_df = total_amount_df.orderBy(col("total_amount").desc())
sorted_spend_df.show()

spark.stop()
