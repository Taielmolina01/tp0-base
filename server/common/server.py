import socket
import logging
import signal
import sys

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self.__acceptor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server 
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
            # TODO: Modify the receive to avoid short-reads
            data = self.__client_socket.recv(1024)
            if not data:
                print("Client has disconnected. Closing socket")
                self.__close_client_socket()
                return
            msg = data.rstrip().decode('utf-8')
            addr = self.__client_socket.getpeername()
            logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')
            # TODO: Modify the send to avoid short-writes
            self.__client_socket.send("{}\n".format(msg).encode('utf-8'))
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
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
            return c
        except OSError:
            self.__handle_exit()

    def __handle_exit(self):
        self.__close_client_socket()
        self.__close_acceptor_socket()
        sys.exit(0)

    def __handle_exit_wrapper(self, signum, frame):
        self.__handle_exit()

    def __close_acceptor_socket(self):
        self.__acceptor_socket.shutdown(socket.SHUT_RDWR)
        self.__acceptor_socket.close()
        logging.info("Closing acceptor socket ...")

    def __close_client_socket(self):
        if self.__client_socket:
            self.__client_socket.shutdown(socket.SHUT_RDWR)
            self.__client_socket.close()
            logging.info("Closing client socket from server ...")
            self.__client_socket = None
