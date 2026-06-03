from pyspark.sql.functions import *

# CREATE DATAFRAME

data = [
(1,"Sravan",25,"Hyderabad","Data Engineer",55000,"2023-01-15","IT"),
(2,"Ravi",28,"Bangalore","Software Engineer",72000,"2022-11-10","IT"),
(3,"Priya",24,"Chennai","Analyst",48000,"2023-03-12","Analytics")
]

columns = [
"emp_id",
"emp_name",
"age",
"city",
"designation",
"salary",
"joining_date",
"department"
]

df = spark.createDataFrame(data, columns)

# SELECT

df.select("emp_name","salary").display()

# ALIAS

df.select(
col("emp_name").alias("employee_name")
).display()

# FILTER

df.filter(
col("salary") > 50000
).display()

# WITHCOLUMNRENAMED

df.withColumnRenamed(
"emp_name",
"employee_name"
).display()

# WITHCOLUMN

df.withColumn(
"bonus",
col("salary") * 0.10
).display()

# TYPECAST

df.withColumn(
"salary",
col("salary").cast("string")
).display()

# SORT

df.orderBy(
col("salary").desc()
).display()

# LIMIT

df.limit(2).display()
