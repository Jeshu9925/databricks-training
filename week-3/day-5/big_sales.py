# READ BIG SALES DATA

df = spark.read.csv(
"/FileStore/tables/Big Sales.csv",
header=True,
inferSchema=True
)

# DISPLAY DATA

display(df)

# SCHEMA

df.printSchema()

# COUNT

print(df.count())

# SHOW SAMPLE DATA

df.show(10)

# COLUMN LIST

print(df.columns)
