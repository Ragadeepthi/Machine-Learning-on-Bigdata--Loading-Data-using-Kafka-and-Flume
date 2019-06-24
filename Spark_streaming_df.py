# Create __SparkSession__ object
# 
#     The entry point to programming Spark with the Dataset and DataFrame API.
# 
#     Used to create DataFrame, register DataFrame as tables and execute SQL over tables etc.

from pyspark.sql import SparkSession

# Import the necessary classes and create a local SparkSession, the starting point of all functionalities related to Spark.
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import col,udf

from pyspark.ml import Pipeline, PipelineModel

spark = SparkSession \
    .builder \
    .appName("Kafka Spark Structured Streaming") \
    .config("spark.master", "local") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Loading the pipeline model
#model = PipelineModel.load("file:///home/2383B49/UberDataShare/KmeansModel/")

#print(model)

# Reading the messsages from the kafka topic and creating a data frame
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "c.insofe.edu.in:9092") \
  .option("subscribe", "2383_PHD_topic2") \
  .option("startingOffsets", "earliest") \
  .load()

df.printSchema()

# Converting the columns to appropriate data types
df = df.select(col("value").cast("string"), col("timestamp"))

# Splitting the value column based on comma delimiter and creating the columns Date,Latitude,Longitude, ID and Status columns
df = df.withColumn('App', split(df.value, "\t")[0])
df = df.withColumn('Category', split(df.value, "\t")[1])
df = df.withColumn('Rating', split(df.value, "\t")[2])
df = df.withColumn('Reviews', split(df.value, "\t")[3])
df = df.withColumn('Size', split(df.value, "\t")[4])
df = df.withColumn('Installs', split(df.value, "\t")[5])
df = df.withColumn('Type', split(df.value, "\t")[6])
df = df.withColumn('Price', split(df.value, "\t")[7])
df = df.withColumn('ContentRating', split(df.value, "\t")[8])
df = df.withColumn('Genres', split(df.value, "\t")[9])
df = df.withColumn('LastUpdated', split(df.value, "\t")[10])
df = df.withColumn('CurrentVer', split(df.value, "\t")[11])
df = df.withColumn('AndroidVer', split(df.value, "\t")[12])

df = df.select('App','Category','Rating', 'Reviews','Size','Installs','Type','Price','ContentRating','Genres','LastUpdated','CurrentVer','AndroidVer','timestamp')


# Writing the predictions to a permanent storage
# Spark structured streaming only supports "parquet" format for now.
# The output mode should be in append mode and also the checkpoint location needs to be mentioned.
query = df \
        .writeStream \
        .format("parquet") \
        .outputMode("append") \
        .option("truncate","false") \
        .option("path", "/user/2383B49/PHD_Bigdata2/results/output") \
        .option("checkpointLocation", "/user/2383B49/PHD_Bigdata2/results/outputCP") \
        .start()

# Start running the query that prints the running counts to the console
# query = test_predictions_lr \
#        .writeStream \
#        .format("console") \
#        .outputMode("append") \
#        .option("truncate","false") \
#        .start()

query.awaitTermination()
