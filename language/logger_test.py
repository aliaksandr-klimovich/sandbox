# https://docs.python.org/2/howto/logging.html#logging-basic-tutorial

import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

# ----------------------------------------
# logger basic config example

logging.basicConfig(
    filename='example.log',
    filemode='a',
    level=logging.INFO,
    format='[%(levelname)s at %(asctime)s]: %(message)s',
    datefmt='%Y-%m-%d %H-%M-%S',
)
