from pyspark.sql import SparkSession
import uuid
import logging
from pyspark.sql.types import StructType, StructField, ArrayType, DoubleType, StringType, LongType
from pyspark.sql.functions import from_json, expr, col, udf
from pyspark.sql.avro.functions import from_avro
from confluent_kafka.schema_registry import SchemaRegistryClient

def get_schema(schema_reg_url=None, subject=None):
    sr = SchemaRegistryClient({'url' : schema_reg_url})
    schema = sr.get_latest_version('live-stock')
    return sr, schema
def create_spark_session():
    print("creaing")
    try:
        session = SparkSession.builder.appName("kafka-stream") \
        .config('spark.jars.packages', "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-avro_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .config("spark.cassandra.connection.port", "9042")  \
        .getOrCreate() 
        session.sparkContext.setLogLevel("ERROR")
        logging.info("connected succesfully")
        print("connnected")
        return session
    except Exception as e:
        logging.error(f'failed to connect err : {e}')
        print("error")

def kafka_conn(conn):
    try:
        df = conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'kafka:9092') \
            .option('subscribe', 'live-stock') \
            .option('startingOffsets', 'earliest') \
            .load()
        df.printSchema()
        df_str = df.selectExpr("CAST(value as STRING) as value")
        df_str.printSchema()
        


        # Define the schema for the 'Trade' record
        trade_schema = StructType([
            StructField("p", DoubleType(), nullable=False),
            StructField("s", StringType(), nullable=False),
            StructField("t", LongType(), nullable=False),
            StructField("v", DoubleType(), nullable=False)
        ])

        # Define the schema for the 'TradeRecord' record
        # avro_schema = StructType([
        #     StructField("data", ArrayType(trade_schema), nullable=False),
        #     StructField("type", StringType(), nullable=False)
        # ])
        
        
        # # json_expanded_df = df_str.withColumn("parsed_value", from_json(df_str["value"], avro_schema)) \
        # #                         .selectExpr("parsed_value.data AS trades", "parsed_value.type AS trade_type")

        # # # Explode the array column 'trades' to get individual trade records
        # # exploded_df = json_expanded_df.selectExpr("explode(trades) AS trade", "trade_type")
        # parsed_df = df_str.withColumn("parsed_value", from_json(df_str["value"], avro_schema)).alias("parsed_value")

        # # Extract fields from parsed_value struct
        # #final_df = parsed_df.selectExpr("parsed_value.data AS trades", "parsed_value.type as trade_type")

        # another_df = parsed_df.selectExpr("explode(parsed_value.data) as trades")
        _, schema_latest = get_schema(schema_reg_url='http://schema-registry:8081', subject='live-stock')
        live_stock_df = df.withColumn("fixed_value", expr("substring(value , 6, len(value) - 5)"))
        # Select columns of interest from the exploded DataFrame
        avro_options = { "mode":"PERMISSIVE"}
        expaned_df = live_stock_df.select(from_avro(col("fixed_value"), schema_latest.schema.schema_str, avro_options)).alias("stock")
        exploded_df = expaned_df.select("stock.from_avro(fixed_value).data", "stock.from_avro(fixed_value).type").alias('decoded_value')
        exploded_df.printSchema()
        data_df = exploded_df.selectExpr("explode(decoded_value.data) as data", "decoded_value.type as type") \
        .select("data.p", "data.s", "data.t", "data.v", "type")
            # data_df = exploded_df.select(
        #     col("decoded_value.data.p").alias("p"),
        #     col("decoded_value.data.s").alias("s"),
        #     col("decoded_value.data.t").alias("t"),
        #     col("decoded_value.data.v").alias("v")
        # )
        btc_data_df = data_df.filter(col("s") == "BINANCE:BTCUSDT").select("p", "s", "t", "v")
        btc_data_df = btc_data_df.withColumnRenamed("p", "price") \
                         .withColumnRenamed("s", "symbol") \
                         .withColumnRenamed("t", "timestamp") \
                         .withColumnRenamed("v", "volume")
        uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())
        btc_data_df_with_id = btc_data_df.withColumn("id", uuid_udf())
        query = btc_data_df_with_id.writeStream \
            .foreachBatch(write_to_cassandra) \
            .outputMode("append") \
            .start()

        query.awaitTermination()
    except Exception as e:
        raise e 
    
def write_to_cassandra(df, epoch_id):
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="trade_data", keyspace="crypto_trades") \
        .mode("append") \
        .save()


# if __name__ == '__main___':
print("invoking")
conn = create_spark_session()
print(conn)
if conn is not None:
    print("here is the schema")
    kafka_conn(conn)