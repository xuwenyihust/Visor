import pytest
import os
import logging
import asyncio
from asyncio import coroutine
import numpy
import datetime
from src.fake_log_gen import fake_log_gen

class access_test(fake_log_gen.fake_access_gen):

	def __init__(self, log, config, mode, heart_num):
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

	def run(self):
		self.loop = asyncio.get_event_loop()
		try:
			self.loop.run_until_complete(
				asyncio.wait([
					#self.heartbeat_lines(),
					#self.access_lines()]
					self.heartbeat_lines()]
				)
			)
		finally:
			self.loop.close()

	@coroutine
	def heartbeat_lines(self):
		for i in range(heart_num):
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')
			self.log.info('- - - [%s] "%s" - -', t, self.config["heartbeat"]["message"])
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

class Log_Gen_Test_Class:

	def __init__(self):
		self.access_file = tmpdir.mkdir("sub").join("access_logs.txt")
		self.error_file = tmpdir.mkdir("sub").join("error_logs.txt")

		# Logs
		self.log = logging.getLogger('Gen')
		logging.basicConfig(level=logging.INFO)

		log_format = logging.Formatter("%(message)s")
		#out = logging.FileHandler('sub/access_logs.txt')
		self.out = logging.FileHandler(self.access_file)
		self.out.setFormatter(log_format)
		self.log.addHandler(self.out)

		# Configs
		with open(os.environ['VISORHOME']+"/config/fake_log_gen.json") as config_file:
			config = json.load(config_file)

	def test_sample(self):
		x = 'this'
		assert 'h' in x

	def test_access_log_heartbeat(self):
		mode = 'access'
		heart_num = 10
		log_gen = access_test(self.log, self.config, mode, heart_num)
		log_gen.run()	

			
		assert self.access_file.read() != ''


