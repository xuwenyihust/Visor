import pytest
import os
import logging
from src.fake_log_gen import fake_log_gen


class Log_Gen_Test_Class:

	def __init__(self):
		p = tmpdir.mkdir("sub").join("access_logs.txt")

		log = logging.getLogger('Gen')
		logging.basicConfig(level=logging.INFO)

		log_format = logging.Formatter("%(message)s")
		out = logging.FileHandler('sub/access_logs.txt')
		out.setFormatter(log_format)
		log.addHandler(out)

	def test_sample(self):
		x = 'this'
		assert 'h' in x

	#def test_access_file_created(self):
	#	p = tmpdir.mkdir("sub").join("access_logs.txt")
	#	gen = fake_log_gen.fake_access_gen()		
