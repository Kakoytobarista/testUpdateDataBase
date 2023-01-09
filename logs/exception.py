import time
from logs.logger import logger


def exception(func):
    def wrapper(*args, **kwargs):
        time_start = time.time()
        try:
            logger.info(f"Function {func.__name__} start")
            logger.info(f"Name of function: '{func.__name__}'")
            logger.info(f'{func.__name__} :: args: {args}')
            logger.info(f'{func.__name__} :: kwargs: {kwargs}')
            result = func(*args, **kwargs)
            logger.info(f'{func.__name__} :: result: {result}'
                        f' in {time.time() - time_start:.2f} sec')
            logger.info(f"Function {func.__name__} finished")
            return result
        except Exception:
            err = f'There was an exception in the {func.__name__}' \
                f' in {time.time() - time_start:.2f} sec'
            logger.exception(err)
            raise
    return wrapper
