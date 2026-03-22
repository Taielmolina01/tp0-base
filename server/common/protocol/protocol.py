from common.blocking_socket.blocking_socket import BlockingSocket
import socket

ACK_CODE = 0x03

class Protocol:
    def __init__(self, sock=None):
        if isinstance(sock, BlockingSocket):
            self.socket = sock
        elif sock is not None:
            self.socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM, sock)
        else:
            self.socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_bet(self):
        _ = self.socket.receive_all(1)
        length = int.from_bytes(self.socket.receive_all(2), byteorder='big')
        bet = self.socket.receive_all(length)
        return bet

    def send_ack_bet(self):
        self.socket.send_all(bytes([ACK_CODE]))

    def getpeername(self):
        return self.socket.sock.getpeername()

    def close(self):
        self.socket.close()