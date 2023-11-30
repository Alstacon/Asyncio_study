import asyncio

import aiohttp
from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str) -> int:
    ten_millis = aiohttp.ClientTimeout(total=1)  # переопределяется таймаут конкретно для get-запроса - 10 мс
    async with session.get(url, timeout=ten_millis) as result:
        return result.status


async def main():
    session_timeout = aiohttp.ClientTimeout(total=2, connect=.1)  # таймаут на уровне клиентского сеанса в 1 секунду,
    # для установления соединение - 100 мс
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        await fetch_status(session, 'https://google.com')


asyncio.run(main())
