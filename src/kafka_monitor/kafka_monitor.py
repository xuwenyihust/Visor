from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


class kafka_monitor(object):

	def __init__(self):
		# Define Spark configuration
		conf = SparkConf()
		conf.setMaster("local[4]")
		conf.setAppName("Kafka Monitor")
		# Initialize a SparkContext
		sc = SparkContext(conf=conf)
		self.ssc = StreamingContext(sc, 10)

		self.addr = 'localhost:9092'
		self.topic = 'TutorialTopic'	

	def run(self):
		lines = KafkaUtils.createDirectStream(self.ssc, [self.topic], {"metadata.broker.list": self.addr})
		#lines.foreachRDD(lambda x: print(x.collect()))

		self.ssc.start()
		self.ssc.awaitTermination()

if __name__=="__main__":
	monitor = kafka_monitor()
	monitor.run()

