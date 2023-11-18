import asyncio


async def delay(time: int) -> int:
    print(f'Засыпаю на {time} секунд')
    await asyncio.sleep(time)
    print(f'Сон в течение {time} секунд закончился')
    return time

