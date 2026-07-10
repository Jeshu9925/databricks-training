from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, col, rank
from pyspark.sql.window import Window
import os
import sys

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Phase3_ETL_Pipeline") \
    .master("local[*]") \
    .getOrCreate()

# Ensure Spark output is less verbose
spark.sparkContext.setLogLevel("ERROR")

# File paths
customers_path = "./samples/customers.csv"
sales_path = "./samples/sales.csv"

# --- Extract ---
print("--- Extract: Reading Data ---")
customers_df = spark.read.csv(customers_path, header=True, inferSchema=True)
sales_df = spark.read.csv(sales_path, header=True, inferSchema=True)

print("\nCustomers Schema:")
customers_df.printSchema()
print("\nSales Schema:")
sales_df.printSchema()

# --- Transform ---
print("\n--- Cleaning Data ---")
# Clean customers: Drop nulls in age and filter invalid age (>0)
clean_customers = customers_df.dropna(subset=["age", "city"]).filter(col("age") > 0)
clean_customers.show()

# Clean sales: Drop nulls in amount
clean_sales = sales_df.dropna(subset=["amount"])

print("\n--- 1. Calculate Daily Sales ---")
daily_sales = clean_sales.groupBy("order_date").agg(sum("amount").alias("daily_sales")).orderBy("order_date")
daily_sales.show()

print("\n--- 2. City-wise Revenue ---")
joined_df = clean_customers.join(clean_sales, "customer_id", "inner")
city_revenue = joined_df.groupBy("city").agg(sum("amount").alias("city_revenue")).orderBy(col("city_revenue").desc())
city_revenue.show()

print("\n--- 3. Find Repeat Customers (>2 orders) ---")
repeat_customers = clean_sales.groupBy("customer_id").agg(count("order_id").alias("order_count")).filter(col("order_count") > 2)
repeat_customers.show()

print("\n--- 4. Find Highest Spending Customer in Each City ---")
customer_spend = joined_df.groupBy("city", "name").agg(sum("amount").alias("total_spend"))
window_spec = Window.partitionBy("city").orderBy(col("total_spend").desc())
highest_spenders = customer_spend.withColumn("rnk", rank().over(window_spec)).filter(col("rnk") == 1).drop("rnk")
highest_spenders.show()

print("\n--- 5. Build Final Reporting Table ---")
final_report = joined_df.groupBy("customer_id", "name", "city") \
    .agg(
        sum("amount").alias("total_spend"),
        count("order_id").alias("order_count")
    ).orderBy(col("total_spend").desc())
final_report.show()

# --- Load / Save Outputs ---
print("\n--- Load: Saving Outputs to Text Files ---")
os.makedirs("outputs", exist_ok=True)

def save_df_to_txt(df, filename):
    try:
        import pandas as pd
        # Using pandas for pretty printing
        pdf = df.toPandas()
        with open(f"outputs/{filename}", "w") as f:
            f.write(pdf.to_string(index=False))
    except ImportError:
        # Fallback if pandas is not installed
        with open(f"outputs/{filename}", "w") as f:
            f.write(df._jdf.showString(100, 20, False))

save_df_to_txt(daily_sales, "1_daily_sales.txt")
save_df_to_txt(city_revenue, "2_city_revenue.txt")
save_df_to_txt(repeat_customers, "3_repeat_customers.txt")
save_df_to_txt(highest_spenders, "4_highest_spenders.txt")
save_df_to_txt(final_report, "5_final_report.txt")

# Also save an overarching output
with open("outputs/all_outputs.txt", "w") as f:
    f.write("=== Daily Sales ===\n")
    f.write(daily_sales._jdf.showString(100, 20, False))
    f.write("\n=== City-wise Revenue ===\n")
    f.write(city_revenue._jdf.showString(100, 20, False))
    f.write("\n=== Repeat Customers (>2 orders) ===\n")
    f.write(repeat_customers._jdf.showString(100, 20, False))
    f.write("\n=== Highest Spenders by City ===\n")
    f.write(highest_spenders._jdf.showString(100, 20, False))
    f.write("\n=== Final Reporting Table ===\n")
    f.write(final_report._jdf.showString(100, 20, False))

print("Outputs saved successfully to the 'outputs' directory.")
spark.stop()
