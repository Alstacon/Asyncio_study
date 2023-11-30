import asyncio
import functools
import time
from typing import Callable, Any


async def delay(time: int) -> int:
    print(f'Засыпаю на {time} секунд')
    await asyncio.sleep(time)
    print(f'Сон в течение {time} секунд закончился')
    return time


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'''Выполняется {func} с аргументами {args} и {kwargs}''')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'''{func} завершилась за {total} с''')

        return wrapped

    return wrapper




