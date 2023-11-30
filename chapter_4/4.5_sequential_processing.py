# Для постепенной обработки приходящих результатов используется as_completed(), которая принимает список объектов,
# допускающих ожидание и возвращает итератор по будущим объектам, их можно перебирать, применяя await
# в этом случае порядок результатов уже не будет детерминирован
import asyncio

import aiohttp

from chapter_4 import fetch_status
from utils import async_timed

async_timed()


async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://gogooole.com', 10),
            fetch_status(session, 'https://google.com', 1),
            fetch_status(session, 'https://google.com', 1),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)  # здесь выполнение приостановится до появления первого результата


asyncio.run(main())


# Постепенная обработка с таймаутом

@async_timed()
async def main_2():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://google.com', 10),
            fetch_status(session, 'https://google.com', 10),
            fetch_status(session, 'https://google.com', 1),
        ]
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('Таймаут')
        for task in asyncio.tasks.all_tasks():
            print(task)


asyncio.run(main_2())
