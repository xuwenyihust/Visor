from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext

import time
import socket


def main(sc):
	
	# Initialize spark streaming context with a batch interval of 10 sec, 
	# The messages would accumulate for 10 seconds and then get processed.
	ssc = StreamingContext(sc, batch_interval)

	# Receive the logs
	host = socket.gethostbyname(socket.gethostname())
	# Create a DStream that represents streaming data from TCP source
	socket_stream = ssc.socketTextStream(host, 5555)
	lines = socket_stream.window(window_time)
	#lines.pprint()
	lines.foreachRDD(lambda x: print(x.collect()))
	#words = lines.flatMap(lambda line: line.split(" "))
	#words.pprint()
	
	# Start the streaming process
	ssc.start()
	#time.sleep(window_time*5)

	process_cnt = 0

	while process_cnt < process_times:
		time.sleep(window_time)				

		process_cnt += 1
	

	ssc.stop()


if __name__=="__main__":
	# Define Spark configuration
	conf = SparkConf()
	conf.setMaster("local[4]")
	conf.setAppName("Stream Analysis")
	# Initialize a SparkContext
	sc = SparkContext(conf=conf)

	batch_interval = 10
	window_time = 10
	process_times = 1

	# Compute the whole time for displaying
	total_time = batch_interval * process_times

	main(sc)


