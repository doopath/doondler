""" A module of server that handles a user. """
import socket


class Server:
    def __init__(self, ip: str = None, port: int = None, clients_count: int = None):
        self.ip = ip or "127.0.0.1"
        self.port = port or 8800
        self.clients_count = clients_count or 1
        self._socket = None
        self._client = None

    def _create_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

    def _handle_client(self):
        client_socket, client_addr = self._socket.accept()
        self._client = {
            "socket": client_socket,
            "address": client_addr
        }

    def _run(self):
        self._create_socket()

        self._socket.bind((self.ip, self.port))
        self._socket.listen(self.clients_count)

        self._handle_client()

    def start(self):
        self._run()

        while True:
            data = self._client["socket"].recv(1024)

            if not data:
                break

            self._client["socket"].send(data)


if __name__ == "__main__":
    server = Server()
    server.start()
