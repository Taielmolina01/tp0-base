from common.blocking_socket.blocking_socket import BlockingSocket
from common.client_handler.client_handler import ClientHandler
import socket
import logging
import signal
import sys

class Server:
    def __init__(self, port, listen_backlog):
        self.__acceptor_socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.__acceptor_socket.bind(('', port))
        self.__acceptor_socket.listen(listen_backlog)
        signal.signal(signal.SIGTERM, self.__handle_exit_wrapper)
        self.__client_handler = None

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """ 
        while True:
            skt = self.__accept_new_connection()
            self.__client_handler = ClientHandler(skt)
            self.__client_handler.run()

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
            return c
        except OSError:
            self.__handle_exit()

    def __handle_exit(self):
        if self.__client_handler:
            self.__client_handler.close()
        self.__close_acceptor_socket()
        sys.exit(0)

    def __handle_exit_wrapper(self, signum, frame):
        self.__handle_exit()

    def __close_acceptor_socket(self):
        self.__acceptor_socket.close()
        logging.info("Closing acceptor socket ...")

