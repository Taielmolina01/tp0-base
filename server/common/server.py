from common.socket.socket import Socket as skt
from common.protocol.protocol import Protocol
import socket
import logging
import signal
import sys

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self.__acceptor_socket = skt(socket.AF_INET, socket.SOCK_STREAM)
        self.__acceptor_socket.bind(('', port))
        self.__acceptor_socket.listen(listen_backlog)
        signal.signal(signal.SIGTERM, self.__handle_exit_wrapper)
        self.__client_socket = None

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """ 
        while True:
            self.__client_socket = self.__accept_new_connection()
            self.__handle_client_connection()

    def __handle_client_connection(self):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            data = self.__client_socket.receive_bet()
            msg = data.rstrip().decode('utf-8')
            addr = self.__client_socket.getpeername()
            logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')
            self.__client_socket.send_ack_bet()
        except ConnectionError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
            logging.error("Client has disconnected. Closing socket")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            self.__close_client_socket()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        try:
            logging.info('action: accept_connections | result: in_progress')
            c, addr = self.__acceptor_socket.accept()
            logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
            return Protocol(c)
        except OSError:
            self.__handle_exit()

    def __handle_exit(self):
        self.__close_client_socket()
        self.__close_acceptor_socket()
        sys.exit(0)

    def __handle_exit_wrapper(self, signum, frame):
        self.__handle_exit()

    def __close_acceptor_socket(self):
        self.__acceptor_socket.close()
        logging.info("Closing acceptor socket ...")

    def __close_client_socket(self):
        if self.__client_socket:
            self.__client_socket.close()
            logging.info("Closing client socket from server ...")
            self.__client_socket = None
