import time
import sys
import threading
import argparse

class mini_monitor(object):

	def __init__(self, logfile):
		self.logfile = logfile
		self.error_cnt = 0

	def analyze(self):
		with open(self.logfile, 'r') as f:
			while True:
				# Remove the trailing \n
				line = f.readline().rstrip()
				if line == '' or line == '\n':
					time.sleep(0.1)
				else:
					self.on_data(line)

	def on_data(self, line):
		# Filter out the HEARTBEAT lines
		if 'HEARBEAT' in line:
			return
		
		#print(line.split('"'))
		# Access log / Error log?
		if line[0] == '[':
			self.on_error_log(line)
		else:
			self.on_access_log(line)

	def on_access_log(self, line):
		return

	def on_error_log(self, line):
		fields = line.split(']')
		fields = [x.strip(' [') for x in fields]
	
		lv = fields[1]

		if lv == 'ERROR':
			self.error_report(fields)		

		return

	def error_report(self, fields):
		self.error_cnt += 1
		print('Total num of errors: ' + str(self.error_cnt))
		print('Error detail: ' + fields[-1])


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="input logfile")
	args = parser.parse_args()
	logfile = args.i
	#print(logfile)
	
	# Instantiate the monitor
	monitor = mini_monitor(logfile)
	# Start the monitoring
	monitor.analyze()

if __name__ == '__main__':
	main()
