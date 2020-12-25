import logging


def get_default_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    log_handler_formatter = logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s',
                                              datefmt='%Y-%m-%dT%H:%M:%S')
    log_handler.setFormatter(log_handler_formatter)
    logger.addHandler(log_handler)
    return logger
