from pyspark.sql.functions import *

# 1 SPLIT DATE
emp_df.withColumn(
"year",
split(col("joining_date"),"-")[0]
).show()

# 2 CONCAT
emp_df.withColumn(
"employee_info",
concat_ws(
"-",
col("name"),
col("department")
)
).show()

# 3 CAST
emp_df.withColumn(
"salary",
col("salary").cast("double")
).show()

# 4 LIT
emp_df.withColumn(
"company",
lit("Capgemini")
).show()

# 5 WHEN
emp_df.withColumn(
"salary_band",
when(
col("salary") > 70000,
"HIGH"
).otherwise("LOW")
).show()

# 6 SUBSTRING
emp_df.select(
substring("name",1,3)
).show()

# 7 REGEXP_REPLACE
emp_df.withColumn(
"designation",
regexp_replace(
"designation",
" ",
"_"
)
).show()

# 8 ISIN
emp_df.filter(
col("city").isin(
"Hyderabad",
"Bangalore"
)
).show()

# 9 BETWEEN
emp_df.filter(
col("salary").between(
50000,
80000
)
).show()
