from common.blocking_socket.blocking_socket import BlockingSocket
from common.utils import Bet
import socket
from server.common.protocol.exceptions.eoc_exception import EndOfCommunicationException
from server.common.protocol.exceptions.bad_amount_fields_bet import (
    BadAmountOfFieldsInBet,
)

ACK_CODE = 0x03
FIN_CODE = 0x05
AMOUNT_OF_FIELDS_BET = 6
AGENCY_FIELD_INDEX = 0
NAME_FIELD_INDEX = 1
LAST_NAME_FIELD_INDEX = 2
DOCUMENT_FIELD_INDEX = 3
BIRTHDATE_FIELD_INDEX = 4
BET_NUMBER_FIELD_INDEX = 5


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
        if code[0] == FIN_CODE:
            raise EndOfCommunicationException()
        return self.__receive_bets()

    def __receive_bets(self):
        length_chunk = self.__receive_big_endian_number()
        bets = []
        for _ in range(length_chunk):
            bets.append(self.__receive_bet())
        return bets

    def __receive_bet(self):
        length = self.__receive_big_endian_number()
        bet_msg = self.socket.receive_all(length)
        return self.__create_bet(str(bet_msg))

    def __create_bet(self, msg):
        real_msg = msg[1 : len(msg) - 1]
        fields = real_msg.split(",")
        if len(fields) != AMOUNT_OF_FIELDS_BET:
            raise BadAmountOfFieldsInBet()
        return Bet(
            fields[AGENCY_FIELD_INDEX],
            fields[NAME_FIELD_INDEX],
            fields[LAST_NAME_FIELD_INDEX],
            fields[DOCUMENT_FIELD_INDEX],
            fields[BIRTHDATE_FIELD_INDEX],
            fields[BET_NUMBER_FIELD_INDEX],
        )

    def send_ack_bet(self):
        self.socket.send_all(bytes([ACK_CODE]))

    def __receive_big_endian_number(self):
        return int.from_bytes(self.socket.receive_all(2), byteorder="big")

    def getpeername(self):
        return self.socket.sock.getpeername()

    def close(self):
        self.socket.close()
