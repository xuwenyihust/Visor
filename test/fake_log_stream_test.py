from src.socket import fake_log_stream
import socket
import random
import json
import logging
import argparse
import asyncio
import datetime
import time
from asyncio import coroutine
import numpy
import threading

class fake_access_stream(object):

	def __init__(self):
		self.mode = 'access'
		self.log = logging.getLogger('Gen')
		logging.basicConfig(level=logging.INFO)
		out = logging.FileHandler('fake_access_stream_test.log')
		log_format = logging.Formatter("%(message)s")
		out.setFormatter(log_format)
		self.log.addHandler(out)

		with open("../config/fake_log_gen.json") as config_file:
			self.config = json.load(config_file)

	def run(self):
		self.log_streamer = fake_log_stream.fake_access_stream(self.log, self.config, self.mode)
		# Run the server
		self.log_streamer.run()



def fake_client():
	print('+++ Fake client starts running!')
	fake_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 5555
	time.sleep(5)
	fake_client.connect((host, port))
	print('+++ Fake Client connected to tested server!')	

	for i in range(5):
		fake_client.recv(1024).decode()

	print('+++ Fake client ends receiving!')
	fake_client.close()


def main():
	#fake_access_stream()
	#time.sleep(2)
	#fake_client()
	client_thread = threading.Thread(target=fake_client)
	client_thread.start()
	time.sleep(1)
	server = fake_access_stream()
	server.run()
	client_thread.join()
	

if __name__ == '__main__':
	main()


