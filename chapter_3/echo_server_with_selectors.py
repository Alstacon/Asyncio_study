import selectors
import socket
from selectors import SelectorKey

selector = selectors.DefaultSelector()

server_socker = socket.socket()
server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socker.bind(('127.0.0.1', 8000))
server_socker.setblocking(False)
server_socker.listen()

selector.register(server_socker, selectors.EVENT_READ)

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)  # создали селектор с таймаутом

    if len(events) == 0:
        print('Пока нет событий, ждем...')

    for event, _ in events:
        event_socket = event.fileobj  # получаем сокет, для которого произошло событие

        if event_socket == server_socker: # если событие произошло с серверным сокетом, значит была попытка подключения
            connection, address = server_socker.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {address}')
            selector.register(connection, selectors.EVENT_READ) # регистрируем в селекторе подключившийся клиент
        else:
            data = event_socket.recv(1024) # если событие произошло не с серверным сокетом — получить данные от клиента и отправить обратно
            print(f'Получены данные: {data}')
            event_socket.send(data)
