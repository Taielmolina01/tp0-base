from common.utils import has_won, load_bets
import logging

AMOUNT_OF_AGENCIES = 5


class Lottery:
    def __init__(self, amount_of_agencies=AMOUNT_OF_AGENCIES):
        self.amount_of_agencies = amount_of_agencies
        self.amount_of_agencies_ready = 0

    def check_agency_as_finished(self):
        self.amount_of_agencies_ready += 1
        return True

    def check_finished(self):
        return self.amount_of_agencies_ready == self.amount_of_agencies
