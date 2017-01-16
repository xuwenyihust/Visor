from setuptools import setup, find_packages

setup(
	version = '0.0',
	author = 'Wenyi Xu',
	packages = find_packages(),
	test_suite = 'tests',
	setup_requires=['pytest-runner'],
	tests_require = ['pytest']
)
