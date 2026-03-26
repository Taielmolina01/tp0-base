from common.blocking_socket.blocking_socket import BlockingSocket
from common.client_handler.client_handler import ClientHandler
from common.lottery.lottery import Lottery
import socket
import logging
import signal
import sys


class Server:
    def __init__(self, port, listen_backlog, amount_of_clients):
        self.__acceptor_socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.__acceptor_socket.bind(("", port))
        self.__acceptor_socket.listen(listen_backlog)
        signal.signal(signal.SIGTERM, self.__handle_exit_wrapper)
        self.__client_handlers: list[ClientHandler] = []
        self.lottery = Lottery(amount_of_clients)
        self.amount_of_clients = amount_of_clients
        self.is_running = True

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        while self.is_running:
            skt = self.__accept_new_connection()
            self.__client_handlers.append(ClientHandler(skt, self.lottery))
            self.__client_handlers[-1].run()
            if self.lottery.check_finished():
                self.__handle_query_phase()
                self.is_running = False

    def __handle_query_phase(self):
        for client in self.__client_handlers:
            if client.had_received_query_winners():
                # Should be always true
                client.inform_agency_result()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        try:
            logging.info("action: accept_connections | result: in_progress")
            c, addr = self.__acceptor_socket.accept()
            logging.info(
                f"action: accept_connections | result: success | ip: {addr[0]}"
            )
            return c
        except OSError:
            self.__handle_exit()

    def __handle_exit(self):
        for client_handler in self.__client_handlers:
            client_handler.close()
        self.__client_handlers = []
        self.__close_acceptor_socket()
        sys.exit(0)

    def __handle_exit_wrapper(self, signum, frame):
        self.__handle_exit()

    def __close_acceptor_socket(self):
        self.__acceptor_socket.close()
        logging.info("Closing acceptor socket ...")
