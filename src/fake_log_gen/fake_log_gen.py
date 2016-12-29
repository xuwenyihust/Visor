# Fake log files generator


import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine


class fake_log_gen(object):

	def __init__(self, log, config, mode):
		self.log = log
		self.mode = mode
		# Dict that contains config info
		self.config = config

	def run(self):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(
			asyncio.wait([
				self.heartbeat_lines()] 
			)
		)
		loop.close()


class fake_access_gen(fake_log_gen):

	def run(self):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(
			asyncio.wait([
				#self.heartbeat_lines(),
				self.access_lines()]
			)
		)
		loop.close()


	@coroutine
	def heartbeat_lines(self):
		while True:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			self.log.info('- - - [%s] "%s" - -', t, self.config["heartbeat"]["message"])
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def access_lines(self):

		access_min = self.config["access"]["interval"]["min"]
		access_max = self.config["access"]["interval"]["max"]

		user_ids = self.config["access"]["user_id"]
		methods = self.config["access"]["method"]
		resources = self.config["access"]["resource"]
		codes = self.config["access"]["code"]
		versions = self.config["access"]["version"]

		while True:
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			user_identifier = 'user-identifier'
			user_id = user_ids[random.randint(0,len(user_ids)-1)]
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')
			msg = methods[random.randint(0, len(methods)-1)]+" "+resources[random.randint(0, len(resources)-1)]+" "+versions[random.randint(0, len(versions)-1)]
			self.log.info('%s %s %s [%s] "%s"', ip, user_identifier, user_id, t, msg)
			yield from asyncio.sleep(random.uniform(access_min, access_max))


class fake_error_gen(fake_log_gen):
	
	def run(self): 
		loop = asyncio.get_event_loop()
		# The event loop
		loop.run_until_complete(
			asyncio.wait([
				self.heartbeat_lines(),
				self.warn_lines(),
				self.error_lines()]
			)
		)
		loop.close()

	@coroutine
	def heartbeat_lines(self):
		while True:
			self.log.info("[-] [-] " + self.config["heartbeat"]["message"])
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def access_lines(self):

		access_min = self.config["access"]["interval"]["min"]
		access_max = self.config["access"]["interval"]["max"]		

		while True:
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			#user_identifier = 
			#user_id =
			self.log.info("%s", ip)
			yield from asyncio.sleep(random.uniform(access_min, access_max)) 
	
	@coroutine
	def warn_lines(self):

		warn_min = self.config["warn"]["interval"]["min"]
		warn_max = self.config["warn"]["interval"]["max"]
		warnings = self.config["warn"]["message"]

		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			self.log.warning("[pid %s:tid %s] [client %s] %s", pid, tid, ip, warnings[random.randrange(len(warnings))])
			yield from asyncio.sleep(random.uniform(warn_min, warn_max))

	@coroutine
	def error_lines(self):
	
		error_min = self.config["error"]["interval"]["min"]
		error_max = self.config["error"]["interval"]["max"]
		errors = self.config["error"]["message"]

		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			self.log.error("[pid %s:tid %s] [client %s] %s", pid, tid, ip, errors[random.randrange(len(errors))])
			yield from asyncio.sleep(random.uniform(error_min, error_max))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("fake_logfile", help="fake logfile")
	parser.add_argument("mode", help="log mode")
	args = parser.parse_args()

	# Identify the log format
	mode = args.mode
	if mode not in ['error', 'access']:
		print('Argument error.')

	# Instantiate the logger
	log = logging.getLogger(None)
	# Set the level
	logging.basicConfig(level=logging.INFO)
	# Instantiate a file Handler
	out = logging.FileHandler(args.fake_logfile)
	# Instantiate a Formatter
	# Format the time string
	if mode == 'error':
		log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%a %b %d %H:%M:%S %Y")
	else:
		log_format = logging.Formatter("%(message)s")
	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	#Test Logging
	'''log.info("INFO!")
	log.error("Error!")
	'''

	# Load the configure json file to a dict
	with open("../config/fake_log_gen.json") as config_file:
		config = json.load(config_file)

	# Instantiate a fake log generator
	if mode == 'error':
		log_gen = fake_error_gen(log, config, mode)
	else:
		log_gen = fake_access_gen(log, config, mode)
	log_gen.run()



if __name__ == "__main__":
	main()


