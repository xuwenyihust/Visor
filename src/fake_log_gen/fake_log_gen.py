# Fake log files generator
#
# Usage:
#	python 3.4 fake_log_gen [fake_logfile]
#
# Format:
#
#  Error log:
#	[Wed Oct 11 14:32:52 2000] [error] [client 127.0.0.1] client denied by server configuration: /export/home/live/ap/htdocs/test


import random
import json
import logging
import argparse
import asyncio
from asyncio import coroutine


class fake_log_gen():
	
	def __init__(self, log, config):
		self.log = log
		self.config = config

	def run(self): 
		loop = asyncio.get_event_loop()
		loop.run_until_complete(
			asyncio.wait([
				self.heartbeat_lines(),
				self.warning_lines()]))
		loop.close()


	@coroutine
	def heartbeat_lines(self):
		while True:
			self.log.info("[-] " + self.config["heartbeat"]["message"])
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))
	
	@coroutine
	def warning_lines(self):

		warn_min = self.config["warning"]["interval"]["min"]
		warn_max = self.config["warning"]["interval"]["max"]
		warnings = self.config["warning"]["message"]

		while True:
			self.log.warning("[client %s] %s", '.'.join(str(random.randint(0, 255)) for i in range(4)), warnings[random.randrange(len(warnings))])
			yield from asyncio.sleep(random.uniform(warn_min, warn_max))

#	def error_lines(self):


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("fake_logfile", help="fake logfile")
	args = parser.parse_args()

	# Instantiate the logger
	log = logging.getLogger(None)
	# Set the level
	logging.basicConfig(level=logging.INFO)
	# Instantiate a file Handler
	out = logging.FileHandler(args.fake_logfile)
	# Instantiate a Formatter
	# Format the time string
	log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%a %b %d %H:%M:%S %Y")
	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	#Test Logging
	'''log.info("INFO!")
	log.error("Error!")
	'''

	# Load the configure json file
	with open("../config/fake_log_gen.json") as config_file:
		config = json.load(config_file)

	# Instantiate a fake log generator
	log_gen = fake_log_gen(log, config)
	log_gen.run()



if __name__ == "__main__":
	main()


