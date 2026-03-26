import socket


class BlockingSocket:
    def __init__(self, address_family, socket_kind, sock=None):
        self.sock = (
            sock if sock is not None else socket.socket(address_family, socket_kind)
        )

    @classmethod
    def with_initialized_socket(cls, sock):
        return cls(socket.AF_INET, socket.SOCK_STREAM, sock=sock)

    def listen(self, listen_backlog):
        self.sock.listen(listen_backlog)

    def bind(self, address):
        self.sock.bind(address)

    def accept(self):
        conn, addr = self.sock.accept()
        return BlockingSocket.with_initialized_socket(conn), addr

    def send_all(self, data):
        sent = 0
        while sent < len(data):
            actual_sent = self.sock.send(data[sent:])
            if actual_sent == 0:
                raise ConnectionError("socket connection broken while sending")
            sent += actual_sent

    def receive_all(self, length):
        data = []
        bytes_received = 0
        while bytes_received < length:
            chunk = self.sock.recv(length - bytes_received)
            if chunk == b"":
                raise ConnectionError("socket connection broken while receiving")
            data.append(chunk)
            bytes_received += len(chunk)
        return b"".join(data)

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
