import logging
import functools
def set_logger():
    logging.basicConfig(filename="logs/logs.txt", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug(f"Running function {func.__name__}")
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

