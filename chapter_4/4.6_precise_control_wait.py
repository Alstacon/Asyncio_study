# Недостатком gather() и as_completed() является сложность со снятием задач, работавших в момент исключения
# Это может привести к падение производительности
# Второй - недетерменированность результатов в as_completed(), из-за этого трудно понять, какая именно задача завершилась

# Эти проблемы решает функция wait(), которая позволяет решить, когда мы хотим получить результаты, возвращает два
# множества: задачи, завершившиеся успешно или в результате исключения и задачи, которые продолжают выполняться,
# позволяет задать таймаут, который не возбуждает исключение
import asyncio
import logging

import aiohttp

from chapter_4 import fetch_status
from utils import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://google.com')),
            asyncio.create_task(fetch_status(session, 'https://google.com')),
        ]

        done, pending = await asyncio.wait(fetchers) # возвращает управление, когда все запросы в fetchers завершатся

        print(f'Выполнено: {len(done)}')
        print(f'Ожидает: {len(pending)}')

        for done_task in done:
            result = await done_task # вот только здесь можно будет увидеть, что в какой-то задаче возникло исключение
            print(result)


# asyncio.run(main())


#  с обработкой исключений методами Task

@async_timed()
async def main_2():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://google.com')),
            asyncio.create_task(fetch_status(session, 'ht://google.com')),
        ]

        done, pending = await asyncio.wait(fetchers)

        print(f'Выполнено: {len(done)}')
        print(f'Ожидает: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error('При выполнении запроса возникло исключение', exc_info=done_task.exception())

asyncio.run(main_2())
