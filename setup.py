from setuptools import setup, find_packages

tests_require = [
	'pytest'
]

setup(
	test_suite = 'tests',
	tests_require=tests_require
)
