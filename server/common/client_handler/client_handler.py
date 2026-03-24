from common.protocol.protocol import Protocol
from common.protocol.exceptions.eoc_exception import EndOfCommunicationException
from common.protocol.exceptions.bad_amount_fields_bet import (
    BadAmountOfFieldsInBet,
)
from common.utils import store_bets
import logging


class ClientHandler:
    def __init__(self, skt, lottery):
        self.is_running = True
        self.__protocol = Protocol(skt)
        self.lottery = lottery
        self.id = self.__protocol.receive_agency_id()
        

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
                    if not self.lottery.check_agency_as_finished(self.id):
                        logging.error(
                            f"action: apuesta_recibida | result: fail | error: bad agency number"
                        )
                    self.is_running = False
                else:   
                    store_bets(data)
                    logging.info(
                        f"action: apuesta_recibida | result: success | cantidad: {self.__repr_bets(data)}"
                    )
                    self.lottery.store_bets_per_agency(self.id, data)
                    self.__protocol.send_ack_bet()
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

    def inform_agency_result(self):
        self.__protocol.send_results_to_agencies(self.lottery.get_winners_of_agency(self.id))
    
    def __repr_bets(self, data):
        return len(data) if data is not None else 0

    def close(self):
        self.__protocol.close()
        logging.info("Closing client socket from server ...")
