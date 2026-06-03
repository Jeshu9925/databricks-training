# 1 REPARTITION
df1 = emp_df.repartition(4)

# 2 COALESCE
df2 = emp_df.coalesce(2)

# 3 CACHE
emp_df.cache()

# 4 FILL NULL
emp_df.fillna(
{
"city":"Unknown"
}
).show()

# 5 REPLACE
emp_df.replace(
"IT",
"Information Technology"
).show()

# 6 DROP NULL
emp_df.na.drop().show()

# 7 RDD MAP
emp_df.rdd.map(
lambda x:
(
x[0],
x[1].upper()
)
).collect()

# 8 CUBE
emp_df.cube(
"department",
"city"
).sum("salary").show()

# 9 ROLLUP
emp_df.rollup(
"department",
"city"
).sum("salary").show()

# 10 BROADCAST JOIN
from pyspark.sql.functions import broadcast

emp_df.join(
broadcast(dept_df),
"department"
).show()
