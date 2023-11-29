import asyncio

import aiohttp


async def fetch_status(session: aiohttp.ClientSession, url: str):
    """
    Посылает get-запрос в переданном сеансе и возвращает статус ответа
    """
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session: # создаем сеанс
        url = 'https://google.com'
        status = await fetch_status(session, url)
        print(f'''Статус код {url} был равен {status}''')


asyncio.run(main())
