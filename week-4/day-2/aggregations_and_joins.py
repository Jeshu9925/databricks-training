from pyspark.sql.functions import *

# 1 AVG SALARY BY DEPARTMENT
emp_df.groupBy(
"department"
).avg("salary").show()

# 2 MAX SALARY BY DEPARTMENT
emp_df.groupBy(
"department"
).max("salary").show()

# 3 TOTAL SALARY
emp_df.agg(
sum("salary")
).show()

department_data = [
("IT","John"),
("HR","Smith"),
("Analytics","Kevin")
]

dept_df = spark.createDataFrame(
department_data,
["department","manager"]
)

# 4 INNER JOIN
emp_df.join(
dept_df,
"department",
"inner"
).show()

# 5 LEFT JOIN
emp_df.join(
dept_df,
"department",
"left"
).show()

# 6 UNION
new_df = emp_df.limit(2)

emp_df.union(new_df).show()

# 7 SAMPLE
emp_df.sample(
0.5
).show()
