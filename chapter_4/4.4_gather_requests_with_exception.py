import asyncio

import aiohttp

from chapter_4 import fetch_status
from utils import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://google.com', 'gg://google.com']
        tasks = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*tasks)
        print(status_codes)


# asyncio.run(main())

# gather не снимает другие работающие задачи при возникновении исключения
# при этом, если произойдет несколько исключений, в конце мы увидим только первое
# чтобы это исправить нужно задать параметр return_exceptions=True


@async_timed()
async def main_2():
    async with aiohttp.ClientSession() as session:
        urls = ['ppp://google.com', 'https://google.com', 'lll://google.com']
        tasks = [fetch_status(session, url) for url in urls]
        # Не нужно явно отлавливать исключения в блоке try/except, потому что в точке await исключение не возбуждается
        status_codes = await asyncio.gather(*tasks, return_exceptions=True)
        print(f'Все: {status_codes}')
        print(f'Исключения: {[res for res in status_codes if isinstance(res, Exception)]}')
        print(f'Успешные: {[res for res in status_codes if not isinstance(res, Exception)]}')


asyncio.run(main_2())
