import time
import logging

from logging.handlers import RotatingFileHandler


def logger_core(error=None, name=None, error_code=500) -> None:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file = "/var/log/hometax/{}.log".format(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    file_handler = RotatingFileHandler(
        filename=file,
        maxBytes=1024 * 1024 * 10,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if error_code >= 500:
        logger.error(error)
    else:
        logger.info(error)
