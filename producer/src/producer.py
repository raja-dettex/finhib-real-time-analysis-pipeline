from confluent_kafka import  SerializingProducer
from confluent_kafka.schema_registry import schema_registry_client
from confluent_kafka.schema_registry.avro import AvroSerializer
import os

class Producer:
    def __init__(self, schema_reg_url, topic_name) -> None:
        self.schema_reg_url = schema_reg_url 
        self.s_client = schema_registry_client.SchemaRegistryClient({'url' : self.schema_reg_url})
        self.schema_str = self.s_client.get_schema(1)
        self.topic_name = topic_name
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')


    def produce(self,data):
        value_serilaizer = AvroSerializer(schema_registry_client=self.s_client, schema_str=self.schema_str)
        producer = SerializingProducer({
            'bootstrap.servers' : 'kafka:9092',
            'value.serializer' : value_serilaizer,
            'delivery.report.only.error' : False
        })
        producer.produce(self.topic_name, value=data,on_delivery=self.delivery_report)
        producer.flush()


    def delivery_report(self, err,msg):
        if err is not None:
            print("error producing to topic {}, err  {}".format(self.topic_name, err))
        else:
            print("produced message to topic : {}, partitions: [{}]".format(msg.topic(), msg.partition()))