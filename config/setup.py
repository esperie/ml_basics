import os
import time
import logging
import django
from pathlib import Path
from colorama import Fore, Style
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict, Any
from django.core.wsgi import get_wsgi_application

PROJECT_PATH = Path(__file__).resolve().parent.parent
PROJECT_NAME = PROJECT_PATH.name
DATA_PATH = PROJECT_PATH / 'store/data'
MODELS_PATH = PROJECT_PATH / 'store/models'
RESULTS_PATH = PROJECT_PATH / 'store/results'
LOG_PATH = Path('logs')
DF_DISPLAY_WIDTH = 0

if os.getcwd() == '/':
	print(f'Changing current working directory from {os.getcwd()}')
	os.chdir(PROJECT_PATH)
	print(f'to {PROJECT_PATH}')

elif os.getcwd() == '/home/ubuntu':
	print(f'Changing current working directory from {os.getcwd()}')
	os.chdir(PROJECT_PATH)
	print(f'to {PROJECT_PATH}')


def initialize_django(
		settings: str = f'{PROJECT_NAME}.settings'):
	# Export Django settings env variable
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

	# Do internal django setup
	if 'setup' in dir(django):
		django.setup()

	# Get Django WSGI app
	django_app = get_wsgi_application()
	return django_app


def get_time(func):
	def timed(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		print(f'{(time.time() - start_time):.4f} secs.')
		return result

	return timed


def setup_logger(name: str, logfile: str = 'test.log'):
	logfile_path = LOG_PATH / logfile
	if not LOG_PATH.exists():
		logfile_path.parent.mkdir()

	# Setup log facility
	logging.basicConfig(
		filename=logfile_path.as_posix(),
		format='%(asctime)s (%(name)s) %(levelname)s: %(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p')
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	# ## add console handler and attach to logger
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)

	# ## create formatter and attach to handler
	formatter = logging.Formatter(
		fmt=f'%(asctime)s {Fore.YELLOW}(%(name)s) {Fore.GREEN}%(levelname)s: {Style.RESET_ALL}%(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p')
	ch.setFormatter(formatter)

	# ## attach console handler to logger
	logger.addHandler(ch)

	return logger
