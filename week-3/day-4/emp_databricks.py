# READ CSV FILE

df = spark.read.csv(
"/FileStore/tables/empData.csv",
header=True,
inferSchema=True
)

# DISPLAY DATA

display(df)

# SCHEMA

df.printSchema()

# ROW COUNT

print(df.count())

# COLUMNS

print(df.columns)
