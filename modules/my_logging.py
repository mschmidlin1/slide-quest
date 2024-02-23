import logging
import logging.config
import functools



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
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/logs.txt',
                'formatter': 'standard',
            },
            'console': {
                'level': 'INFO',
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

    logging.config.dictConfig(LOGGING_CONFIG)

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

