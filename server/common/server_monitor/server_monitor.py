from common.utils import store_bets, load_bets, has_won
from threading import Lock

class ServerMonitor:
    def __init__(self):
        self.lock = Lock()

    def store_bets_safe(self, bets):
        with self.lock:
            store_bets(bets)

    def load_bets_safe(self):
        with self.lock:
            return load_bets()