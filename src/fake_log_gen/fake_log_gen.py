# Fake log files generator
#
# Usage:
#	python 3.4 fake_log_gen [fake_logfile]
#
# Log Format:
#	127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
#
# Fields:
#	IP address
#	RFC 1413  identity of the client
#	UserID
#	Date, time, timezone
#	Request
#	HTTP status code
#	Size of the object returned to the client

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
				self.common_lines()]))
		loop.close()


	@coroutine
	def common_lines(self):
		while True:
			self.log.info("INFO!")
			yield from asyncio.sleep(3.0)

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
	log_format = logging.Formatter()
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


