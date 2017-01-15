import pytest
import os
import logging
from src.fake_log_gen import fake_log_gen


class Log_Gen_Test_Class:

	def __init__(self):
		access_file = tmpdir.mkdir("sub").join("access_logs.txt")
		error_file = tmpdir.mkdir("sub").join("error_logs.txt")

		# Logs
		log = logging.getLogger('Gen')
		logging.basicConfig(level=logging.INFO)

		log_format = logging.Formatter("%(message)s")
		#out = logging.FileHandler('sub/access_logs.txt')
		out = logging.FileHandler(access_file)
		out.setFormatter(log_format)
		log.addHandler(out)

		# Configs
		with open(os.environ['VISORHOME']+"/config/fake_log_gen.json") as config_file:
			config = json.load(config_file)

	def test_sample(self):
		x = 'this'
		assert 'h' in x

	#def test_access_file_created(self):
	#	p = tmpdir.mkdir("sub").join("access_logs.txt")
	#	gen = fake_log_gen.fake_access_gen()		
