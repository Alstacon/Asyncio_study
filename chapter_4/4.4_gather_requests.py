# gather принимает последовательность допускающих ожидание объектов и запускает их конкурентно
# если среди объектов есть корутина - gather обертывает ее задачей, чтобы гарантировать конкурентное выполнение
import asyncio

import aiohttp

from chapter_4 import fetch_status


async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://google.com' for _ in range(1000)]
        requests = [
            await fetch_status(session, url) for url in urls  # здесь генерируется список корутин для каждого запроса
        ]
        # при этом независимо от очередности завершения корутин, результаты будут переданы в том же порядке,
        # в каком передавались объекты
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


asyncio.run(main())
