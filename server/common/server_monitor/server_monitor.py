from common.utils import store_bets
from threading import Lock


class ServerMonitor:
    def __init__(self):
        self.lock = Lock()

    def store_bets_safe(self, bets):
        with self.lock:
            store_bets(bets)
