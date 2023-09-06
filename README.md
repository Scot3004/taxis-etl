# ETL project

This project has been designed as starting point to understand and learn  about ETL process.
ETL stands for Extract, Transform and Load, and the main idea of this project is to use open data available about the
New York cities taxis to create an ETL, so you will extract the data from "parquet" files, load the data in memory and
transform the read data into a new one.

## Data

Data dictionaries and datasets can be found in the NYC page: [NYC Portal](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Scenarios

Considered scenarios in the project:

### Case 1: Travel time according location

Using the columns:

* `tpep_pickup_datetime`
* `tpep_dropoff_datetime`
* `Trip_distance`
* `PULocationID`
* `DOLocationID`

### Case 2: Payment by distance

* Using the columns:
* `PULocationID`
* `DOLocationID`
* `Trip_distance`
* `Tolls_amount`
* `Total_amount`

### Case 3: Payment by time

* Using the columns:
* `tpep_pickup_datetime`
* `tpep_dropoff_datetime`
* `Passenger_count`
* `Payment_type`
* `Total_amount`

## Install

To be able to run this project you should have a properly configured environment. The instructions below contains the required
steps you should follow to be able to run the entire project.

### Install java (Linux, Mac, WSL)

Install [sdkman](https://sdkman.io/) and activate the environment

```bash
curl -s "https://get.sdkman.io" | bash
# Inside the project folder install java, spark and hadoop (required once)
sdk env install
# Then you can simply enable the environment with
sdk env
```

### Install python dependencies

We recommend to use a virtual env with python

```bash
python -m venv venv
```

And then install the dependencies, -e in the custom folder reads the pyproject.toml

```bash
pip install -e .
```

## Running the project

Setup the following environment variables

TAXIS_ETL_FILES, TAXIS_ETL_DOWNLOAD_FOLDER, TAXIS_ETL_BASE_URL, TAXIS_ETL_DOWNLOAD_FILES

Files from S3

```bash
export TAXIS_ETL_FILES=yellow_tripdata_2020-01.parquet,yellow_tripdata_2021-01.parquet,yellow_tripdata_2022-01.parquet
export TAXIS_ETL_DOWNLOAD_FOLDER=downloads
export TAXIS_ETL_BUCKET_NAME=s3-bucket
```

Set AWS credentials

Set the aws credentials for pyspark running the commands

```bash
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
```

> if you're running from a devcontainer, check if the value of the aws credentials is passed by printing the value with the command `echo $AWS_ACCESS_KEY_ID`

### Execution

Executing the etl is possible with the command `spark-submit`

When we have a simple script that get the data from spark we can run it passing the python script

```bash
spark-submit src/taxis_etl_prft/SimpleApp.py
```

But if your package depends in something external, for example s3a from hadoop-aws, you will need to load the package to the spark instance, in this scenario,
you will need provide the packages for example we run it with the command

```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 src/taxis_etl_prft/DemoS3.py
```

### By

* Santiago Ruiz
* Diego Peña

## Workarounds

### Java exception Class org.apache.hadoop.fs.s3a.S3AFileSystem not found

If you see this exception in the logs when you run the spark submit command

```bash
java.lang.RuntimeException: java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found
```

Please ensure that you're providing the packages in the `spark-submit` command

### Java exception org.apache.hadoop.fs.s3a.auth.NoAuthWithAWSException

If you see this exception in the logs when you run the spark submit command

```yaml
Caused by: org.apache.hadoop.fs.s3a.auth.NoAuthWithAWSException: 
No AWS Credentials provided by TemporaryAWSCredentialsProvider SimpleAWSCredentialsProvider EnvironmentVariableCredentialsProvider IAMInstanceCredentialsProvider 
: com.amazonaws.SdkClientException: Unable to load AWS credentials from environment variables (AWS_ACCESS_KEY_ID (or AWS_ACCESS_KEY) and AWS_SECRET_KEY (or AWS_SECRET_ACCESS_KEY))
```

Do the configuration for aws credentials with aws cli

> IMPORTANT is not enough for some reason the aws configure and requred to export the variables to the environment

Export aws credentials (this can be done after aws configuration)

```bash
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
```

# java.lang.NoSuchFieldError: JAVA_9

if you see the exception line

```sh
py4j.protocol.Py4JJavaError: An error occurred while calling None.org.apache.spark.api.java.JavaSparkContext.
: java.lang.NoSuchFieldError: JAVA_9
```

Enable the java 11 from sdkman

# ModuleNotFoundError: No module named 'dotenv'

This appears when your environment has not installed the python deps see the section "Install python dependencies"