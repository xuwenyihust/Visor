from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import os
import smtplib
#from smtplib import SMTP_SSL as SMTP
#from email.mime.text import MIMEText


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

	def error_alert(self):
		'''text = 'An error occurs!'
		msg = MIMEText(text, 'plain')
		msg['Subject'] = "Error detected"
		# Send the email to where?
		me = 'wenyixu101@gmail.com'
		msg['To'] = me
		try:	
			conn = SMTP('localhost')
			conn.set_debuglevel(True)
			conn.login(self.config['email']['address'], self.config['email']['password'])
			try:
				conn.sendmail(me, me, msg.as_string())
			finally:
				conn.close()
		except:
			print('Unable to send email!')'''

		TO = 'wenyixu101@gmail.com'
		SUBJECT = 'TEST MAIL'
		TEXT = 'Here is a message from python.'
	
		# Gmail Sign In
		gmail_sender = 'visorannouncement@gmail.com'
		gmail_passwd = 'omg876dqbi@dfs'

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
		useful_lines = val_lines.filter(lambda x: 'HEARTBEAT' not in x)

		error_lines = val_lines.filter(lambda x: 'ERROR' in x)

		#error_lines.foreachRDD(lambda x: print(x.collect()))
		error_lines.foreachRDD(lambda x: self.error_alert())

		self.ssc.start()
		self.ssc.awaitTermination()

if __name__=="__main__":
	# Load the configurations
	with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as config_file:
		config = json.load(config_file)

	monitor = kafka_monitor(config)
	monitor.run()

