import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создание сокета
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # настройка переиспользования номера порта

server_socket.bind(('127.0.0.1', 8000))

server_socket.listen()  # начинаем прослушивать сокет
server_socket.setblocking(False)
connections = []

try:
    while True:
        try:
            connection, client_address = server_socket.accept()  # блокирует программу до получения запроса, потом возвращает объект
            # подключения (еще один сокет для чтения данных от клиента и отправки данных ему)
            # и адрес подключившегося клиента
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {client_address}')
            connections.append(connection)
        except BlockingIOError:
            pass
        for connect in connections:
            try:
                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = connect.recv(2)
                    if not data:
                        break
                    else:
                        print(f'Получены данные {data}')
                        buffer = buffer + data
                print(f'Все данные {buffer}')
                connect.send(buffer)
            except BlockingIOError:
                pass

finally:
    server_socket.close()
