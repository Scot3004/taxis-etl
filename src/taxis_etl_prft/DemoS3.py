import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, unix_timestamp

from functools import reduce


load_dotenv()

conf = SparkConf()
conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262')
spark = SparkSession.builder.appName("DemoS3").config(conf=conf).getOrCreate()

bucket = os.getenv("AWS_S3_BUCKET")
print("Bucket {}".format(bucket))
filenames = os.getenv("TAXIS_ETL_FILES").split(",")

parquets = map(lambda key: spark.read.parquet("s3a://{}/{}".format(bucket, key)), filenames)
joined_parquets = reduce(lambda x, y: x.union(y), parquets)

trip_distance_km = joined_parquets.withColumn("trip_Distance_kms", col("trip_distance") * 1.6)
final_transform = trip_distance_km.withColumn("travel_time",
      (unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))) / 60)

final_transform.write.option("delimiter", "\t").option("header", "true").mode("overwrite").csv("results/csv")

spark.stop()
