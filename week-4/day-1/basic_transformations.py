# 1. SELECT NAME AND SALARY
emp_df.select("name","salary").show()

# 2. SELECT EMP_ID DEPARTMENT CITY
emp_df.select("emp_id","department","city").show()

# 3. FILTER SALARY > 70000
emp_df.filter(emp_df.salary > 70000).show()

# 4. FILTER IT EMPLOYEES
emp_df.filter(emp_df.department=="IT").show()

# 5. ADD BONUS COLUMN
from pyspark.sql.functions import *

emp_df.withColumn(
"bonus",
col("salary")*0.10
).show()

# 6. RENAME COLUMN
emp_df.withColumnRenamed(
"emp_id",
"employee_id"
).show()

# 7. DROP AGE
emp_df.drop("age").show()

# 8. DISTINCT DEPARTMENTS
emp_df.select("department").distinct().show()

# 9. SORT BY SALARY DESC
emp_df.orderBy(col("salary").desc()).show()

# 10. LIMIT 3 RECORDS
emp_df.limit(3).show()
