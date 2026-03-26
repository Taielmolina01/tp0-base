from common.blocking_socket.blocking_socket import BlockingSocket
from common.utils import Bet
import socket
from common.protocol.eoc_exception import EndOfCommunicationException

ACK_CODE = 0x03
FIN_CODE = 0x05


class Protocol:
    def __init__(self, sock=None):
        if isinstance(sock, BlockingSocket):
            self.socket = sock
        elif sock is not None:
            self.socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM, sock)
        else:
            self.socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_operation(self):
        code = self.socket.receive_all(1)
        if code == FIN_CODE:
            raise EndOfCommunicationException()
        return self.__receive_bet()

    def __receive_bet(self):
        length = int.from_bytes(self.socket.receive_all(2), byteorder="big")
        bet_msg = self.socket.receive_all(length)
        return self.__create_bet(str(bet_msg))

    def __create_bet(self, msg):
        real_msg = msg[1 : len(msg) - 1]
        fields = real_msg.split(",")
        return Bet(0, fields[0], fields[1], fields[2], fields[3], fields[4])

    def send_ack_bet(self):
        self.socket.send_all(bytes([ACK_CODE]))

    def getpeername(self):
        return self.socket.sock.getpeername()

    def close(self):
        self.socket.close()
