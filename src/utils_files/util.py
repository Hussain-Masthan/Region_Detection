import logging
import os
import time


# Create a logger based on module name
_LOGGER = logging.getLogger(__name__)


def setup_root_logger(prefix: str):
    """
    Creates a root logger which logs all INFO messages to a file given a prefix
    The log file name is returned.
    """

    # Generate logging file
    log_root = os.getcwd() + '/logger/'
    # if os.getenv("PYTHON_LOG_ROOT") is None:
    #     raise RuntimeError("Environment variable PYTHON_LOG_ROOT is not set! Exiting..")
    # curr_time = time.localtime()
    # log_file = "%s/%s_%04d%02d%02d-%02d%02d%02d.log" % (
    #     log_root,
    #     prefix,
    #     curr_time.tm_year,
    #     curr_time.tm_mon,
    #     curr_time.tm_mday,
    #     curr_time.tm_hour,
    #     curr_time.tm_min,
    #     curr_time.tm_sec)
    log_file = f'{log_root}/{prefix}.log'
    # Set root logger to send all INFO messages to a log file
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %H:%M:%S")
    ch = logging.FileHandler(log_file)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.INFO)
    return log_file


class MigrationException(Exception):
    """ Class to handle exception raised during the migration process
    """
    pass




