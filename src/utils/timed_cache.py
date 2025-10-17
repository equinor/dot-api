from functools import lru_cache, wraps
from datetime import datetime, timedelta, timezone
from typing import Callable, TypeVar, Any, Optional, cast

F = TypeVar('F', bound=Callable[..., Any])

def timed_lru_cache(seconds: int, maxsize: Optional[int] = None) -> Callable[[F], F]:

    def wrapper_cache(func: F) -> F:
        cached_func = lru_cache(maxsize=maxsize)(func)
        cached_func.lifetime = timedelta(seconds=seconds)  # type: ignore
        cached_func.expiration = datetime.now(timezone.utc) + cached_func.lifetime  # type: ignore

        @wraps(func)
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            if datetime.now(timezone.utc) >= cached_func.expiration:  # type: ignore
                cached_func.cache_clear()  # type: ignore
                cached_func.expiration = datetime.now(timezone.utc) + cached_func.lifetime  # type: ignore

            return cached_func(*args, **kwargs)

        return cast(F, wrapped_func)

    return wrapper_cache