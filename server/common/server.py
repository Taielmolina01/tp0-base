from common.blocking_socket.blocking_socket import BlockingSocket
from common.client_handler.client_handler import ClientHandler
from common.lottery.lottery import Lottery
from common.lottery.lottery_monitor import LotteryMonitor
from common.server_monitor.server_monitor import ServerMonitor
import socket
import logging
import signal
import sys
from threading import Thread, Barrier

class Server:
    def __init__(self, port, listen_backlog, amount_of_clients):
        self.__acceptor_socket = BlockingSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.__acceptor_socket.bind(("", port))
        self.__acceptor_socket.listen(listen_backlog)
        signal.signal(signal.SIGTERM, self.__handle_exit_wrapper)
        self.__client_handlers : list[ClientHandler] = []
        self.__client_threads: list[Thread] = []
        self.lottery_monitor = LotteryMonitor(Lottery(amount_of_clients))
        self.amount_of_clients = amount_of_clients
        self.is_running = True
        self.barrier = Barrier(amount_of_clients)
        self.server_monitor = ServerMonitor()

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        while self.is_running:
            skt = self.__accept_new_connection()
            self.__client_handlers.append(ClientHandler(skt, self.lottery_monitor, self.server_monitor, self.barrier))
            self.__client_threads.append(Thread(target=self.__client_handlers[-1].run))
            self.__client_threads[-1].start()
        
        self.lottery_monitor.check_finished()
        self.__handle_query_phase()

        for thread in self.__client_threads:
            thread.join()

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
