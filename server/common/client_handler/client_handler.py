from common.protocol.protocol import Protocol
from common.protocol.exceptions.eoc_exception import EndOfCommunicationException
from common.protocol.exceptions.bad_amount_fields_bet import (
    BadAmountOfFieldsInBet,
)
from common.utils import store_bets, load_bets, has_won
from common.lottery.lottery import Lottery
import logging
from threading import Barrier
from common.server_monitor.server_monitor import ServerMonitor


class ClientHandler:
    def __init__(self, 
                skt, 
                lottery: Lottery,
                server_monitor: ServerMonitor,
                barrier: Barrier, 
                ):
        self.is_running = True
        self.__protocol = Protocol(skt)
        self.lottery: Lottery = lottery
        self.id = self.__protocol.receive_agency_id()
        self.barrier = barrier
        self.server_monitor = server_monitor

    def run(self):
        """
        Read message from a specific client socket and closes the socket
        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        while self.is_running:
            try:
                data, ended = self.__protocol.receive_operation()
                if ended:
                    if not self.lottery.check_agency_as_finished():
                        logging.error(
                            f"action: apuesta_recibida | result: fail | error: bad agency number"
                        )
                    self.is_running = False
                else:   
                    self.server_monitor.store_bets_safe(data)
                    logging.info(
                        f"action: apuesta_recibida | result: success | cantidad: {self.__repr_bets(data)}"
                    )
                    self.__protocol.send_ack_bet()
                    self.barrier.wait()
            except EndOfCommunicationException:
                self.is_running = False
            except BadAmountOfFieldsInBet as e:
                self.is_running = False
                logging.info(
                    f"action: apuesta_recibida | result: success | cantidad: {self.__repr_bets(data)}"
                )
            except ValueError as e:
                self.is_running = False
                logging.info(
                    f"action: apuesta_recibida | result: success | cantidad: {self.__repr_bets(data)}"
                )
            except ConnectionError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
                logging.error("Client has disconnected. Closing socket")
                self.is_running = False
            except OSError as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
                self.is_running = False
        self.inform_agency_result()
        self.close()

    def inform_agency_result(self):
        self.__protocol.send_results_to_agency([int(bet.document) for bet in self.server_monitor.load_bets_safe() if bet.agency == self.id and has_won(bet)])
    
    def had_received_query_winners(self):
        return self.__protocol.had_received_query_winners()

    def __repr_bets(self, data):
        return len(data) if data is not None else 0

    def close(self):
        self.__protocol.close()
        logging.info("Closing client socket from server ...")
