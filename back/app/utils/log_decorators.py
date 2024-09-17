import asyncio
import functools
import logging
import time

from app.dependencies.settings import get_settings

settings = get_settings()
logger = logging.getLogger("App")
logger.setLevel(settings.logging.level)


def log_deco(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            truncated_args = [
                f"{str(arg)[:settings.logging.debug_arg_length]}..."
                if len(str(arg)) > settings.logging.debug_arg_length
                else arg
                for arg in args
            ]
            truncated_kwargs = {
                k: f"{str(v)[:settings.logging.debug_arg_length]}..."
                if len(str(v)) > settings.logging.debug_arg_length
                else v
                for k, v in kwargs.items()
            }
            logger.info(f"Calling {f.__name__} ...")
            logger.debug(
                f"Entering function {f.__name__} with args: {truncated_args} and kwargs: {truncated_kwargs}",
            )
            result = f(*args, **kwargs)
            truncated_result = (
                f"{str(result)[:settings.logging.debug_arg_length]}..."
                if len(str(result)) > settings.logging.debug_arg_length
                else result
            )
            logger.debug(
                f"Exiting function {f.__name__} with result: {truncated_result}",
            )
            return result
        except Exception as e:
            extra_info = kwargs.get("extra_info", "No extra info provided.")
            logger.exception(
                f"Exception occurred in function {f.__name__}. Extra info: {extra_info}",
                exc_info=settings.app.stacktrace,
            )
            raise e
        finally:
            elapsed_time = time.time() - start_time
            logger.debug(f"Function {f.__name__} took {elapsed_time:.4f} seconds")

    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            truncated_args = [
                f"{str(arg)[:settings.logging.debug_arg_length]}..."
                if len(str(arg)) > settings.logging.debug_arg_length
                else arg
                for arg in args
            ]
            truncated_kwargs = {
                k: f"{str(v)[:settings.logging.debug_arg_length]}..."
                if len(str(v)) > settings.logging.debug_arg_length
                else v
                for k, v in kwargs.items()
            }
            logger.info(f"Calling {f.__name__} ...")
            logger.debug(
                f"Entering function {f.__name__} with args: {truncated_args} and kwargs: {truncated_kwargs}",
            )
            if asyncio.iscoroutinefunction(f):
                result = await f(*args, **kwargs)
            else:
                result = f(*args, **kwargs)
            truncated_result = (
                f"{str(result)[:settings.logging.debug_arg_length]}..."
                if len(str(result)) > settings.logging.debug_arg_length
                else result
            )
            logger.debug(
                f"Exiting function {f.__name__} with result: {truncated_result}",
            )
            return result
        except Exception as e:
            extra_info = kwargs.get("extra_info", "No extra info provided.")
            logger.error(
                f"Exception occurred in function {f.__name__}. Extra info: {extra_info}",
                exc_info=settings.app.stacktrace,
            )
            raise e
        finally:
            elapsed_time = time.time() - start_time
            logger.debug(f"Function {f.__name__} took {elapsed_time:.4f} seconds")

    if asyncio.iscoroutinefunction(f):
        return async_wrapper
    return wrapper
