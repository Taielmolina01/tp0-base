from common.protocol.protocol import Protocol
from server.common.protocol.exceptions.eoc_exception import EndOfCommunicationException
from server.common.protocol.exceptions.bad_amount_fields_bet import (
    BadAmountOfFieldsInBet,
)
from common.utils import store_bets
import logging


class ClientHandler:
    def __init__(self, skt):
        self.is_running = True
        self.__protocol = Protocol(skt)

    def run(self):
        """
        Read message from a specific client socket and closes the socket
        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        while self.is_running:
            try:
                data = self.__protocol.receive_operation()
                bets = store_bets(data)
                logging.info(
                    f"action: apuesta_recibida | result: success | cantidad: {len(bets)}"
                )
                self.__protocol.send_ack_bet()
            except EndOfCommunicationException:
                self.is_running = False
            except BadAmountOfFieldsInBet as e:
                self.is_running = False
                logging.info(
                    f"action: apuesta_recibida | result: success | cantidad: {len(bets)}"
                )
            except ValueError as e:
                self.is_running = False
                logging.info(
                    f"action: apuesta_recibida | result: success | cantidad: {len(bets)}"
                )
            except ConnectionError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
                logging.error("Client has disconnected. Closing socket")
                self.is_running = False
            except OSError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
                self.is_running = False
        self.close()

    def close(self):
        self.__protocol.close()
        logging.info("Closing client socket from server ...")
