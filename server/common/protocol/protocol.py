from common.blocking_socket.blocking_socket import BlockingSocket
from common.utils import Bet
import socket
from common.protocol.exceptions.eoc_exception import EndOfCommunicationException
from common.protocol.exceptions.bad_amount_fields_bet import (
    BadAmountOfFieldsInBet,
)
import logging

ACK_CODE = 0x03
FIN_CODE = 0x05
FIN_CHUNKS_CODE = 0x10
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

    def receive_agency_id(self):
        return self.socket.receive_all(1)[0]

    def receive_operation(self):
        code = self.socket.receive_all(1)
        if code[0] == FIN_CHUNKS_CODE:
            return [], True
        else:
            return self.__receive_bets(), False
        
    def send_results_to_agencies(self, winners):
        self.__send_big_endian_two_bytes_number(len(winners))
        for winner in winners:
            self.__send_big_endian_four_bytes_number(winner)

    def send_ack_bet(self):
        self.socket.send_all(bytes([ACK_CODE]))

    def getpeername(self):
        return self.socket.sock.getpeername()

    def close(self):
        self.socket.close()

    ## Helpers

    def __receive_bets(self):
        length_chunk = self.__receive_big_endian_number()
        bets = []
        for _ in range(length_chunk):
            bets.append(self.__receive_bet())
        return bets

    def __receive_bet(self):
        length = self.__receive_big_endian_number()
        bet_msg = self.socket.receive_all(length)
        return self.__create_bet(bet_msg.decode("utf-8").strip())

    def __create_bet(self, msg):
        fields = msg.split(",")
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
    
    def __send_big_endian_two_bytes_number(self, number):
        self.socket.send_all(number.to_bytes(2, byteorder='big'))

    def __send_big_endian_four_bytes_number(self, number):
        self.socket.send_all(number.to_bytes(4, byteorder='big'))
    
    def __receive_big_endian_number(self):
        return int.from_bytes(self.socket.receive_all(2), byteorder="big")