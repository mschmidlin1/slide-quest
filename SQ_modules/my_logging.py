import logging
from logging.config import dictConfig
import functools
from SQ_modules.configs import FILE_LOG_LEVEL, STDOUT_LOG_LEVEL
import os

#check for log folder and logs file and create if they don't exist.
if not os.path.isdir("logs"):
    os.mkdir("logs")
if not os.path.isfile("logs/logs.txt"):
    with open('logs/logs.txt', 'w') as file: 
        pass

def set_logger():
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': FILE_LOG_LEVEL,
                'class': 'logging.FileHandler',
                'filename': 'logs/logs.txt',
                'formatter': 'standard',
            },
            'console': {
                'level': STDOUT_LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',  # Use standard output
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['file', 'console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }

    dictConfig(LOGGING_CONFIG)

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug(f"Running function {func.__name__}")
            result = func(*args, **kwargs)
            logging.debug(f"Completed function {func.__name__}")
            return result
        except Exception as e:
            logging.error(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

