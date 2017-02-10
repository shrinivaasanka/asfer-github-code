from pyspark.sql import SparkSession

spark=SparkSession.builder.appName("Spark SQL query").getOrCreate()
df = spark.sql("SELECT * FROM words")
df.show()
