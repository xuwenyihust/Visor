# Fake log files generator
# Usage:
#	python 3.4 fake_log_gen [fake_logfile]

import random
import logging
import argparse


#class fake_log_gen():
	
#	def __init__(self):
		

#	def run(): 
		

#	def common_lines():


#	def warning_lines();


#	def error_lines():


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

	### Test Logging
	log.info("INFO!")
	log.error("Error!")

	# Instantiate a fake log generator
	#log_gen = fake_log_gen()

	#log_gen.run()



if __name__ == "__main__":
	main()


