from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

#def main():



if __name__=="__main__":
	# Define Spark configuration
	conf = SparkConf()
	conf.setMaster("local[4]")
	conf.setAppName("Stream Analysis")
	# Initialize a SparkContext
	sc = SparkContext(conf=conf)

	#batch_interval = 10
	#window_time = 10
	#process_times = 1

	# Compute the whole time for displaying
	#total_time = batch_interval * process_times

	#main(sc)

	ssc = StreamingContext(sc, 10)

	#zkQuorum, topic = sys.argv[1:]
	zkQuorum = 'localhost:9092'
	topic = 'TutorialTopic'
	kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": 'localhost:9092'})
	kvs.foreachRDD(lambda x: print(x.collect()))
	#lines = kvs.map(lambda x: x[1])
	#counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
	#counts.pprint()
	#kvs.pprint()

	ssc.start()
	ssc.awaitTermination()	




