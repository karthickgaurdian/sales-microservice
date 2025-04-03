import asyncio
import functools
import logging
from typing import Any, Callable, Type, Union, Tuple

from core.config_sample import settings
from core.constants_sample import (
    MAX_RETRIES,
    RETRY_DELAY,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING
)

logger = logging.getLogger(__name__)

def async_retry(
    max_retries: int = MAX_RETRIES,
    delay: int = RETRY_DELAY,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
) -> Callable:
    """
    Retry decorator for async functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exceptions: Exception(s) to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}. "
                            f"Retrying in {wait_time} seconds..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed. Last error: {str(e)}"
                        )
                        raise last_exception
            
            raise last_exception
        
        return wrapper
    return decorator 