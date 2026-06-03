from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Week4Day1").getOrCreate()

employee_data = [
(101,"Sravan","Data Engineer","IT",75000,"Hyderabad",28,"2021-05-10","Male"),
(102,"Ravi","Software Engineer","IT",68000,"Bangalore",30,"2020-03-15","Male"),
(103,"Priya","Data Analyst","Analytics",62000,"Chennai",26,"2022-01-12","Female"),
(104,"Kiran","Manager","HR",90000,"Mumbai",35,"2018-07-19","Male"),
(105,"Anjali","HR Executive","HR",45000,"Pune",24,"2023-02-20","Female")
]

columns = [
"emp_id","name","designation","department",
"salary","city","age","joining_date","gender"
]

emp_df = spark.createDataFrame(employee_data, columns)
