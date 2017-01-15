import pytest
import os
import sys
import logging
import asyncio
from asyncio import coroutine
import numpy
import datetime
import time
import json
import random
from src.fake_log_gen import fake_log_gen

class access_test(fake_log_gen.fake_access_gen):

	def __init__(self, log, config, mode, heart_num, access_num):
		self.log = log
		self.mode = mode
		# Dict that contains config info
		self.config = config

		self.access_min = self.config["access"]["interval"]["min"]
		self.access_max = self.config["access"]["interval"]["max"]
		self.user_ids = self.config["access"]["user_id"]
		self.methods = self.config["access"]["method"]
		self.methods_dist = self.config["access"]["method_dist"]
		self.resources = self.config["access"]["resource"]
		self.codes = self.config["access"]["code"]
		self.codes_dist = self.config["access"]["code_dist"]
		self.versions = self.config["access"]["version"]

		# Uniquely in testing
		self.heart_num = heart_num
		self.access_num = access_num

	def run(self):
		self.loop = asyncio.get_event_loop()
		try:
			self.loop.run_until_complete(
				asyncio.wait([
					self.access_lines(),
					self.heartbeat_lines()]
				)
			)
		finally:
			self.loop.close()

	@coroutine
	def heartbeat_lines(self):
		for i in range(self.heart_num):
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')
			self.log.info('- - - [%s] "%s" - -', t, self.config["heartbeat"]["message"])
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def access_lines(self):
		for i in range(self.access_num):
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			user_identifier = '-'
			user_id = self.user_ids[random.randint(0,len(self.user_ids)-1)]
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')

			method = numpy.random.choice(self.methods, p=self.methods_dist)
			resource = self.resources[random.randint(0, len(self.resources)-1)]
			version = self.versions[random.randint(0, len(self.versions)-1)]
			msg = method + " " + resource + " " + version
			code = numpy.random.choice(self.codes, p=self.codes_dist)
			size = random.randint(1024, 10240)
			self.log.info('%s %s %s [%s] "%s" %s %s', ip, user_identifier, user_id, t, msg, code, size)
			yield from asyncio.sleep(random.uniform(self.access_min, self.access_max))


class Test_Log_Gen:

	def test_access_log_heartbeat(self):	
		f = os.environ['VISORHOME']+"/tests/tmp/"+"access_logs_test.txt"
		with open(f, "w+") as access_file:
			# Logs
			log = logging.getLogger('Gen')
			logging.basicConfig(level=logging.INFO)

			log_format = logging.Formatter("%(message)s")
			out = logging.FileHandler(f)
			out.setFormatter(log_format)
			log.addHandler(out)

			# Configs
			with open(os.environ['VISORHOME']+"/config/fake_log_gen.json") as config_file:
				config = json.load(config_file)


			mode = 'access'
			heart_num = 10
			access_num = 100
			log_gen = access_test(log, config, mode, heart_num, access_num)
			log_gen.run()	
			
			sample_line = '127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
			line_size = sys.getsizeof(sample_line)
	
			lines = access_file.readlines(line_size*100)	
			total_num = len(lines)
			heart_num_res = len([line for line in lines if 'HEARTBEAT' in line])			
			methods_dist = config["access"]["method_dist"]
			access_get = len([line for line in lines if 'GET' in line])
			access_post = len([line for line in lines if 'POST' in line])
			access_put = len([line for line in lines if 'PUT' in line])
			access_delete = len([line for line in lines if 'DELETE' in line])
			access_total = access_get + access_post + access_put + access_delete			

			access_get_dist = access_get / access_total
			access_post_dist = access_post / access_total
			access_put_dist = access_put / access_total
			access_delete_dist = access_delete / access_total
			# Can produce HEARTBEAT lines?
			assert heart_num_res == heart_num
			# Conform the predefined dist?
			assert self.in_range(access_get_dist, methods_dist[0]) 
			assert self.in_range(access_post_dist, methods_dist[1])
			assert self.in_range(access_put_dist, methods_dist[2])
			assert self.in_range(access_delete_dist, methods_dist[3])

	
	def in_range(self, x, y):
		return float(x/y) >= 0.7 and float(x/y) <= 1.3



