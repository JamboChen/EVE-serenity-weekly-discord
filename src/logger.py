# logger.py
import logging


def configure_logging(log_level):
    log_format = "[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s"
    logging.basicConfig(format=log_format, level=log_level)


def get_logger(name) -> logging.Logger:
    return logging.getLogger(name)
