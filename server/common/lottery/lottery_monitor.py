from common.lottery.lottery import Lottery
from threading import Lock
from common.utils import store_bets, load_bets, has_won


class LotteryMonitor:
    def __init__(self, lottery: Lottery):
        self.lottery: Lottery = lottery
        self.lock = Lock()

    def check_agency_as_finished(self):
        with self.lock:
            return self.lottery._check_agency_as_finished()

    def check_finished(self):
        with self.lock:
            return self.lottery._check_finished()

    def get_winners_of_agency(self, agency_number):
        with self.lock:
            return self.lottery._get_winners_of_agency(agency_number)
