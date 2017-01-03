import unittest
from src import fake_log_gen

class fake_log_gen_test(unittest.TestCase):

	def test_101(self):
		self.assertEqual(2, 1+1)

	

if __name__ == '__main__':
	unittest.main()
