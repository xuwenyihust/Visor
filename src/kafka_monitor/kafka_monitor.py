from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import os
import smtplib
import time
import datetime


class kafka_monitor(object):

	def __init__(self, config, config_private):
		# Load config file
		self.config = config
		# Load private config file
		self.config_private = config_private
		# Define Spark configuration
		conf = SparkConf()
		conf.setMaster(self.config['master_url'])
		conf.setAppName(self.config['app_name'])
		conf.set("num-executors", "3")
		# Initialize a SparkContext
		sc = SparkContext(conf=conf)
		# Set the batch interval to be 1 sec
		self.ssc = StreamingContext(sc, self.config['batch_interval'])

		# Set the Kafka related params
		self.addr = self.config['kafka']['addr']
		self.topic = self.config['kafka']['topic']	

		# Set the summary report params
		# report interval: in terms of sec
		self.report_interval = self.config['email']['report']['interval']
		# The batch interval may also be used aside the sparkstreamingcontext creation
		self.batch_interval = self.config['batch_interval']	

		# Count the total number of logs
		# Used in summary report system
		self.total_log_num = 0

		# Pick out the top ips in all logs
		self.top_ips=[('None', 0) for i in range(3)]
		# Pick out the top ips in [ERROR] logs
		self.top_error_ips=[('None', 0) for i in range(3)]

	
	# Send an email every time detects an error log
	def error_alert_email(self, error):
		# In case of empty list
		# Check if the report system is on
		if len(error) > 0 and self.config['email']['alert']['on']:
			# Parse the error	
			error_li = error[0].split(']')
			error_time = error_li[0].lstrip('[')
			error_process = error_li[2].lstrip().lstrip('[')
			error_client = error_li[3].split(' ')[2]
			error_msg = error_li[4].rstrip('\n')	

			TO = self.config['email']['alert']['receiver']
			SUBJECT = self.config['email']['alert']['subject']
			TEXT = '''
An error occurred in the cluster.

Time: %s

Process: %s

Client: %s

Message: %s
		''' % (error_time, error_process, error_client, error_msg) 
	
			# Sender Gmail Sign In
			gmail_sender = self.config_private['email']['address']
			gmail_passwd = self.config_private['email']['password']

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

	
	
	# Send an email every pre-defined time (30 min / 2 hrs / 1 day ...)
	# to report the summary
	def summary_report_email(self, errors, error_cnt):
		if self.config['email']['report']['on']:
			TO = self.config['email']['report']['receiver']
			SUBJECT = self.config['email']['report']['subject']
			TEXT = '''
Basic:

	Log count:
	- {lc}

	Error count:
	- {ec}

	Error rate:
	- {er: .2f}%

Statistics:

	Log import rate:
	- {lr: .2f} per sec

	Top ip addresses:
	- {top_ip_0}: {top_ip_0_num}
	- {top_ip_1}: {top_ip_1_num}
	- {top_ip_2}: {top_ip_2_num}

	Top error ip addresses:
	- {top_eip_0}: {top_eip_0_num}
    - {top_eip_1}: {top_eip_1_num}
    - {top_eip_2}: {top_eip_2_num}

			'''.format(lc = self.total_log_num, \
					   ec = error_cnt, \
					   er = error_cnt/self.total_log_num*100, \
					   lr = self.total_log_num/self.report_interval, \
					   top_ip_0 = self.top_ips[0][0], \
					   top_ip_0_num = self.top_ips[0][1], \
					   top_ip_1 = self.top_ips[1][0], \
					   top_ip_1_num = self.top_ips[1][1], \
					   top_ip_2 = self.top_ips[2][0], \
					   top_ip_2_num = self.top_ips[2][1], \
					   top_eip_0 = self.top_error_ips[0][0], \
					   top_eip_0_num = self.top_error_ips[0][1], \
                       top_eip_1 = self.top_error_ips[1][0], \
                       top_eip_1_num = self.top_error_ips[1][1], \
                       top_eip_2 = self.top_error_ips[2][0], \
                       top_eip_2_num = self.top_error_ips[2][1] \
					  )

		
			# Sender Gmail Sign In
			gmail_sender = self.config_private['email']['address']
			gmail_passwd = self.config_private['email']['password']

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
		lines = KafkaUtils.createDirectStream(self.ssc, [self.topic], {"metadata.broker.list": self.addr})	
		# Performe lines.foreachRDD(lambda x: print(x.collect()))
		# Get: [(None, '[-] [-] HEARTBEAT\n'), (None, '[-] [-] HEARTBEAT\n'), (None, '[-] [-] HEARTBEAT\n')]	[(None, '[-] [-] HEARTBEAT\n'), (None, '[-] [-] HEARTBEAT\n'), (None, '[-] [-] HEARTBEAT\n')] ...	

		# Extract the valuable log from the tuple, discard 'None'  
		val_lines = lines.map(lambda x: x[1])
		val_lines.cache()
		# Performe val_lines.foreachRDD(lambda x: print('val_lines:', x.collect()))
		# Get: ['[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n']

		# Filter out the error logs
		error_lines = val_lines.filter(lambda x: 'ERROR' in x)

		# Every time an error occurs, send an alert email	
		error_lines.foreachRDD(lambda x: self.error_alert_email(x.collect()))

		# Use val_sum_lines to store all log lines in the window
		# val_sum_lines.count() will be used as the total num of logs in the window
		# Same window size as error_sum_lines, but slides much faster to update faster	
		val_sum_lines = val_lines.window(self.report_interval, self.batch_interval)
		# Performe val_sum_lines.foreachRDD(lambda x: print(x.collect()))
		# Get: ['[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n', '[-] [-] HEARTBEAT\n' ...]

		# SUM(*) GROUP BY client ip address (from all log lines except HAERTBEAT)
		# SORT BY SUM(*)
		val_sum_lines_top_ip = val_sum_lines.filter(lambda x: 'HEARTBEAT' not in x) \
											.map(lambda x: (x.split(']')[3].lstrip(' ').lstrip('[client '),1)) \
											.reduceByKey(lambda x, y: x+y) \
											.map(lambda x: (x[1], x[0])) \
											.transform(lambda x: x.sortByKey()) \
											.map(lambda x: (x[1], x[0]))

		# From val_sum_lines_top_ip, get the top 3 client ip addresses
		# Assign them to List self.top_ips
		def get_top_ips(val_sum_lines_top_ip):
			if val_sum_lines_top_ip.count() > 3:
				self.top_ips = val_sum_lines_top_ip.take(3)
			else:
				self.top_ips[:val_sum_lines_top_ip.count()] = val_sum_lines_top_ip.collect()
			return
	
		val_sum_lines_top_ip.foreachRDD(get_top_ips)
		#val_sum_lines_top_ip.pprint()

		# Window the error lines
		error_sum_lines = error_lines.window(self.report_interval, self.report_interval)

		# SUM(*) GROUP BY client ip address (from [ERROR] lines)
		error_sum_lines_top_ip = error_sum_lines.map(lambda x: (x.split(']')[3].lstrip(' ').lstrip('[client '),1)) \
												.reduceByKey(lambda x, y: x+y) \
												.map(lambda x: (x[1], x[0])) \
												.transform(lambda x: x.sortByKey()) \
												.map(lambda x: (x[1], x[0]))

		# From error_sum_lines_top_ip, get the top 3 client ip addresses
		# Assign them to List self.top_error_ips
		def get_top_error_ips(error_sum_lines_top_ip):
			if error_sum_lines_top_ip.count() > 3:
				self.top_error_ips = error_sum_lines_top_ip.take(3)
			else:
				self.top_error_ips[:error_sum_lines_top_ip.count()] = error_sum_lines_top_ip.collect()
			return

		error_sum_lines_top_ip.foreachRDD(get_top_error_ips)

		# Generate summary report every window time
		error_sum_lines.foreachRDD(lambda x: self.summary_report_email(x.collect(), x.count()))
	
		def get_total_log_num(val_sum_lines):
			self.total_log_num = val_sum_lines.count()
			return 

		# Collect the total number of logs in the current window	
		val_sum_lines.foreachRDD(get_total_log_num)
	
		#####################################################
		# Start the streaming process
		self.ssc.start()	
		self.ssc.awaitTermination()


if __name__=="__main__":
	# Load the configurations
	with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as config_file:
		config = json.load(config_file)

	# Load private email information
	with open(os.environ['VISORHOME']+"/config/private.json") as private_file:
		config_private = json.load(private_file)

	monitor = kafka_monitor(config, config_private)
	monitor.run()

