# Имеется одна сопрограмма, listen_for_connection, прослушивающая порт.
# Как только клиент подключился, она запускает задачу echo для этого клиента,
# которая ожидает поступления данных и отправляет их обратно клиенту.

import asyncio
import logging
import signal
from asyncio import AbstractEventLoop
import socket
from typing import Set


class GracefullExit(SystemExit):
    pass


def shutdown():
    raise GracefullExit()


async def close_echo_tasks(echo_tasks: list[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


def cancel_task():
    print('Получен сигнал SIGINT')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Снимаем {len(tasks)} задач')
    [task.cancel() for task in tasks]


async def echo(connection: socket.socket, loop: AbstractEventLoop):
    """
    Это корутины, получающая и отправляющая данные назад клиенту
    """
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('Получены данные')
            if data == b'boom\r\n':
                raise Exception('Неожиданная ошибка')
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


echo_tasks = []


async def listen_for_connections(server_socket: socket.socket, loop: AbstractEventLoop):
    """
    Корутина для прослушивания порта
    """
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен сообщение от {address}')
        task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(task)


async def main() -> None:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('127.0.0.1', 8000))
    server_socket.setblocking(False)
    server_socket.listen()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await listen_for_connections(server_socket, loop)


loop = asyncio.new_event_loop()
loop.add_signal_handler(signal.SIGINT, shutdown)

try:
    loop.run_until_complete(main())
except GracefullExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
