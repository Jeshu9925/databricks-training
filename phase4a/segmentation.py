from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, when, percent_rank
from pyspark.sql.window import Window
from pyspark.ml.feature import Bucketizer

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Phase4A_Bucketing") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load and prepare data
print("=== Phase 4A: Bucketing & Segmentation ===")
customers = spark.read.option("header", "true").csv("samples/customers.csv", inferSchema=True)
sales = spark.read.option("header", "true").csv("samples/sales.csv", inferSchema=True)

# Calculate total spend per customer
customer_spend = sales.groupBy("customer_id").agg(sum("amount").alias("total_spend"))
df = customers.join(customer_spend, "customer_id", "inner").select("customer_id", "name", "total_spend")
print("\n--- Base Customer Spend Data ---")
df.show()

# Method 1: Conditional Logic (when)
print("\n--- Method 1: Conditional Logic (Gold/Silver/Bronze) ---")
df_when = df.withColumn(
    "segment_when",
    when(col("total_spend") > 10000, "Gold")
    .when((col("total_spend") >= 5000) & (col("total_spend") <= 10000), "Silver")
    .otherwise("Bronze")
)
df_when.show()

# Grouping by segment to count customers (Practice Task 2)
print("Customer Count by Segment (Method 1):")
df_when.groupBy("segment_when").count().show()


# Method 2: SQL CASE Statement
print("\n--- Method 2: SQL CASE Statement ---")
df.createOrReplaceTempView("customer_data")
df_sql = spark.sql("""
    SELECT customer_id, name, total_spend,
        CASE 
            WHEN total_spend > 10000 THEN 'Gold'
            WHEN total_spend >= 5000 AND total_spend <= 10000 THEN 'Silver'
            ELSE 'Bronze'
        END AS segment_sql
    FROM customer_data
""")
df_sql.show()


# Method 3: Bucketizer (MLlib)
print("\n--- Method 3: Bucketizer (MLlib) ---")
# 0.0 to 5000 (bucket 0), 5000 to 10000 (bucket 1), > 10000 (bucket 2)
splits = [-float("inf"), 5000, 10000, float("inf")]
bucketizer = Bucketizer(splits=splits, inputCol="total_spend", outputCol="bucket")
df_bucket = bucketizer.transform(df)

# Map buckets to labels for clarity
df_bucket = df_bucket.withColumn(
    "segment_ml",
    when(col("bucket") == 2.0, "Gold")
    .when(col("bucket") == 1.0, "Silver")
    .when(col("bucket") == 0.0, "Bronze")
)
df_bucket.show()


# Method 4: Quantile-based Segmentation
print("\n--- Method 4: Quantile-based Segmentation ---")
quantiles = df.approxQuantile("total_spend", [0.33, 0.66], 0)
print(f"Calculated Quantiles (33rd, 66th): {quantiles}")

p33 = quantiles[0]
p66 = quantiles[1]

df_quantile = df.withColumn(
    "segment_quantile",
    when(col("total_spend") >= p66, "High")
    .when((col("total_spend") >= p33) & (col("total_spend") < p66), "Medium")
    .otherwise("Low")
)
df_quantile.show()


# Method 5: Window-based Ranking
print("\n--- Method 5: Window-based Ranking ---")
window = Window.orderBy(col("total_spend").desc())
df_window = df.withColumn("rank_pct", percent_rank().over(window))

df_window = df_window.withColumn(
    "segment_rank",
    when(col("rank_pct") <= 0.33, "Top 33%")
    .when((col("rank_pct") > 0.33) & (col("rank_pct") <= 0.66), "Middle 33%")
    .otherwise("Bottom 33%")
)
df_window.show()

spark.stop()
