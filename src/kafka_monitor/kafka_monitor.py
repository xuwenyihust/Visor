from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import os
import smtplib


class kafka_monitor(object):

	def __init__(self, config):
		# Load config file
		self.config = config
		# Define Spark configuration
		conf = SparkConf()
		conf.setMaster("local[4]")
		conf.setAppName("Kafka Monitor")
		# Initialize a SparkContext
		sc = SparkContext(conf=conf)
		# Set the batch interval to be 1 sec
		self.ssc = StreamingContext(sc, 1)

		self.addr = 'localhost:9092'
		self.topic = 'TutorialTopic'	

	def error_alert_email(self, error):
		if len(error) > 0:
		# Parse the error	
			error_li = error[0].split(']')
			error_time = error_li[0].lstrip('[')
			error_client = error_li[3].split(' ')[2]
			error_msg = error_li[4].rstrip('\n')	

			TO = 'wenyixu101@gmail.com'
			SUBJECT = 'Error Alert'
			TEXT = '''
An error occurred in the cluster.

time: %s

client: %s

message: %s
		''' % (error_time, error_client, error_msg) 
	
			# Gmail Sign In
			gmail_sender = self.config['email']['address']
			gmail_passwd = self.config['email']['password']

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login(gmail_sender, gmail_passwd)

			BODY = '\r\n'.join(['To: %s' % TO,'From: %s' % gmail_sender,'Subject: %s' % SUBJECT,'', TEXT])

			try:	
				server.sendmail(gmail_sender, [TO], BODY)
				print ('email sent')
			except:
				print ('error sending mail')

			server.quit()

	def run(self):
		# Consume Kafka streams directly, without receivers
		lines = KafkaUtils.createDirectStream(self.ssc, [self.topic], {"metadata.broker.list": self.addr}).window(10, 10)
		#lines.foreachRDD(lambda x: print(x.collect()))
		val_lines = lines.map(lambda x: x[1])
		#val_lines.foreachRDD(lambda x: print(x.collect()))
		#useful_lines = val_lines.filter(lambda x: 'HEARTBEAT' not in x)

		error_lines = val_lines.filter(lambda x: 'ERROR' in x)
							   #.map(lambda x: x.split(']'))

		#error_lines.foreachRDD(lambda x: print(x.collect()))
		error_lines.foreachRDD(lambda x: self.error_alert_email(x.collect()))

		self.ssc.start()
		self.ssc.awaitTermination()

if __name__=="__main__":
	# Load the configurations
	with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as config_file:
		config = json.load(config_file)

	monitor = kafka_monitor(config)
	monitor.run()

