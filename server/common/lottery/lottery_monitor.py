from lottery.lottery import Lottery 
from threading import Lock

class LotteryMonitor:
    def __init__(self, lottery: Lottery):
        self.lottery = lottery
        self.lock = Lock()

    def check_agency_as_finished(self, agency_number):
        with self.lock:
            self.lottery.__check_agency_as_finished(agency_number)
    
    def store_bets_per_agency(self, agency_id, bets):
        with self.lock:
            self.lottery.__store_bets_per_agency(agency_id, bets)
    
    def check_finished(self):
        with self.lock:
            self.lottery.__check_finished()

    def get_winners_of_agency(self, agency_number):
        with self.lock:
            self.lottery.__get_winners_of_agency(agency_number)