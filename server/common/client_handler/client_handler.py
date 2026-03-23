from common.protocol.protocol import Protocol
from common.utils import store_bets
import logging

class ClientHandler:
    def __init__(self, skt):
        self.__protocol = Protocol(skt)

    def run(self):
        """
        Read message from a specific client socket and closes the socket
        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            data = self.__protocol.receive_bet()
            store_bets([data])
            logging.info(f"action: apuesta_almacenada | result: success | dni: {data.document} | numero: {data.number}")            
            self.__protocol.send_ack_bet()
        except ConnectionError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
            logging.error("Client has disconnected. Closing socket")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            self.__close_client_socket()

    def close(self):
        self.__protocol.close()
        logging.info("Closing client socket from server ...")