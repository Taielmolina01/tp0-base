from common.socket.socket import Socket as skt
import socket

ACK_CODE = 0x03

class Protocol:
    def __init__(self):
        self.socket = skt(socket.AF_INET, socket.SOCK_STREAM)

    def receive_bet(self):
        _ = self.socket.receive_all(1)
        length = socket.ntohs(self.socket.receive_all(2))
        bet = self.socket.receive_all(length)
        return bet

    def send_ack_bet(self):
        self.socket.send_all(ACK_CODE)