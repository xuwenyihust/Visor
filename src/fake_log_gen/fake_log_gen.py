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
import logging
import argparse
import asyncio
from asyncio import coroutine


class fake_log_gen():
	
	def __init__(self, log):
		self.log = log

	def run(self): 
		loop = asyncio.get_event_loop()
		loop.run_until_complete(
			asyncio.wait([
				self.heartbeat_lines()]))
		loop.close()


	@coroutine
	def heartbeat_lines(self):
		while True:
			self.log.info("[-] HEARTBEAT")
			yield from asyncio.sleep(3.0)
	
#	@coroutine
#	def warning_lines(self);


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
	log_format = logging.Formatter("[%(asctime)s][%(levelname)s]%(message)s", "%a %b %d %H:%M:%S %Y")
	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	#Test Logging
	'''log.info("INFO!")
	log.error("Error!")
	'''

	# Instantiate a fake log generator
	log_gen = fake_log_gen(log)

	log_gen.run()



if __name__ == "__main__":
	main()


