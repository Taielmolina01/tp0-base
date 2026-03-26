from common.protocol.protocol import Protocol
from common.protocol.eoc_exception import EndOfCommunicationException
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
                store_bets([data])
                logging.info(
                    f"action: apuesta_almacenada | result: success | dni: {data.document} | numero: {data.number}"
                )
                self.__protocol.send_ack_bet()
            except EndOfCommunicationException as e:
                self.is_running = False
            except ConnectionError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
                logging.error("Client has disconnected. Closing socket")
            except OSError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
        self.close()

    def close(self):
        self.__protocol.close()
        logging.info("Closing client socket from server ...")
