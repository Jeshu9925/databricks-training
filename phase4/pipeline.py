from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, col, when
from pyspark.sql.types import IntegerType, DoubleType
import os

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Phase4_Mini_Project") \
    .master("local[*]") \
    .getOrCreate()

# Set log level to minimize verbosity
spark.sparkContext.setLogLevel("ERROR")

# File paths
customers_path = "./samples/customers.csv"
sales_path = "./samples/sales.csv"

print("=== Phase 4: Data Pipeline & Analytics ===")

# --- Extract ---
print("\n--- Extracting Data ---")
customers_df = spark.read.option("header", "true").csv(customers_path, inferSchema=True)
sales_df = spark.read.option("header", "true").csv(sales_path, inferSchema=True)

print("Original Customers Count:", customers_df.count())
print("Original Sales Count:", sales_df.count())

# --- Transform / Data Cleaning ---
print("\n--- Cleaning Data ---")

# Check and enforce column types
customers_df = customers_df.withColumn("customer_id", col("customer_id").cast(IntegerType()))
sales_df = sales_df.withColumn("customer_id", col("customer_id").cast(IntegerType())) \
                   .withColumn("amount", col("amount").cast(DoubleType())) \
                   .withColumn("order_id", col("order_id").cast(IntegerType()))

# 1. Remove rows with null keys
clean_customers = customers_df.dropna(subset=["customer_id"])
clean_sales = sales_df.dropna(subset=["customer_id", "order_id"])

# 2. Remove duplicate rows
clean_customers = clean_customers.dropDuplicates()
clean_sales = clean_sales.dropDuplicates()

# 3. Filter invalid values (negative amounts)
clean_sales = clean_sales.filter(col("amount") > 0)

print("Cleaned Customers Count:", clean_customers.count())
print("Cleaned Sales Count:", clean_sales.count())

# --- Business Logic & Tasks ---

# Task 1: Daily Sales → Output: date, total_sales
print("\n--- Task 1: Daily Sales ---")
daily_sales = clean_sales.groupBy("order_date") \
                          .agg(sum("amount").alias("total_sales")) \
                          .withColumnRenamed("order_date", "date") \
                          .orderBy("date")
daily_sales.show()

# Join clean datasets for further customer analytics
joined_df = clean_sales.join(clean_customers, "customer_id", "inner")

# Task 2: City-wise Revenue → Output: city, total_revenue
print("\n--- Task 2: City-wise Revenue ---")
city_revenue = joined_df.groupBy("city") \
                         .agg(sum("amount").alias("total_revenue")) \
                         .orderBy(col("total_revenue").desc())
city_revenue.show()

# Task 3: Top 5 Customers → Output: customer_name, total_spend
print("\n--- Task 3: Top 5 Customers ---")
top_5_customers = joined_df.groupBy("name") \
                           .agg(sum("amount").alias("total_spend")) \
                           .withColumnRenamed("name", "customer_name") \
                           .orderBy(col("total_spend").desc()) \
                           .limit(5)
top_5_customers.show()

# Task 4: Repeat Customers (>1 order) → Output: customer_id, order_count
print("\n--- Task 4: Repeat Customers ---")
repeat_customers = clean_sales.groupBy("customer_id") \
                               .agg(count("order_id").alias("order_count")) \
                               .filter(col("order_count") > 1) \
                               .orderBy(col("order_count").desc())
repeat_customers.show()

# Task 5: Customer Segmentation → total_spend > 10000 → Gold, 5000–10000 → Silver, <5000 → Bronze
# Output: customer_name, total_spend, segment
print("\n--- Task 5: Customer Segmentation ---")
customer_spend = joined_df.groupBy("name") \
                           .agg(sum("amount").alias("total_spend")) \
                           .withColumnRenamed("name", "customer_name")

customer_segmentation = customer_spend.withColumn(
    "segment",
    when(col("total_spend") > 10000, "Gold")
    .when((col("total_spend") >= 5000) & (col("total_spend") <= 10000), "Silver")
    .otherwise("Bronze")
).orderBy(col("total_spend").desc())
customer_segmentation.show()

# Task 6: Final Reporting Table → Combine all insights
# Output: customer_name, city, total_spend, order_count, segment
print("\n--- Task 6: Final Reporting Table ---")
customer_report = joined_df.groupBy("customer_id", "name", "city") \
                           .agg(
                               sum("amount").alias("total_spend"),
                               count("order_id").alias("order_count")
                           )

final_df = customer_report.withColumn(
    "segment",
    when(col("total_spend") > 10000, "Gold")
    .when((col("total_spend") >= 5000) & (col("total_spend") <= 10000), "Silver")
    .otherwise("Bronze")
).select(
    col("name").alias("customer_name"),
    col("city"),
    col("total_spend"),
    col("order_count"),
    col("segment")
).orderBy(col("total_spend").desc())
final_df.show()

# --- Load / Save Outputs ---
print("\n--- Task 7: Save Output ---")
# Save final dataframe as CSV into samples/output/report
final_df.write.mode("overwrite").option("header", "true").csv("./samples/output/report")
print("Saved final_df output to './samples/output/report'")

# Save helper txt files inside outputs/ directory for verification (similar to phase3)
os.makedirs("outputs", exist_ok=True)

def save_df_to_txt(df, filename):
    try:
        import pandas as pd
        pdf = df.toPandas()
        with open(f"outputs/{filename}", "w") as f:
            f.write(pdf.to_string(index=False))
    except ImportError:
        with open(f"outputs/{filename}", "w") as f:
            f.write(df._jdf.showString(100, 20, False))

save_df_to_txt(daily_sales, "1_daily_sales.txt")
save_df_to_txt(city_revenue, "2_city_revenue.txt")
save_df_to_txt(top_5_customers, "3_top_5_customers.txt")
save_df_to_txt(repeat_customers, "4_repeat_customers.txt")
save_df_to_txt(customer_segmentation, "5_customer_segmentation.txt")
save_df_to_txt(final_df, "6_final_report.txt")

# Create overarching file
with open("outputs/all_outputs.txt", "w") as f:
    f.write("=== Task 1: Daily Sales ===\n")
    f.write(daily_sales._jdf.showString(100, 20, False))
    f.write("\n=== Task 2: City-wise Revenue ===\n")
    f.write(city_revenue._jdf.showString(100, 20, False))
    f.write("\n=== Task 3: Top 5 Customers ===\n")
    f.write(top_5_customers._jdf.showString(100, 20, False))
    f.write("\n=== Task 4: Repeat Customers ===\n")
    f.write(repeat_customers._jdf.showString(100, 20, False))
    f.write("\n=== Task 5: Customer Segmentation ===\n")
    f.write(customer_segmentation._jdf.showString(100, 20, False))
    f.write("\n=== Task 6: Final Reporting Table ===\n")
    f.write(final_df._jdf.showString(100, 20, False))

print("All outputs saved successfully in 'outputs/' directory.")
spark.stop()
