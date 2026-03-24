from common.utils import has_won, load_bets
import logging

AMOUNT_OF_AGENCIES = 5

class Agency:
    def __init__(self, id):
        self.id = id
        self.is_ready = False
        self.winners = []
        self.bets = {} 

    def __repr__(self):
        return f"{{id: {self.id}; winners: {self.winners}; bets: {self.bets}}}"

class Lottery:
    def __init__(self, amount_of_agencies=AMOUNT_OF_AGENCIES):
        self.amount_of_agencies = amount_of_agencies
        self.agencies = {i: Agency(i) for i in range(1, self.amount_of_agencies+1)}
        self.amount_of_agencies_ready = 0

    def check_agency_as_finished(self, agency_number):
        actual = self.agencies.get(agency_number, False)
        if not actual:
            return False
        self.agencies[agency_number].is_ready = True
        self.amount_of_agencies_ready += 1
        return True
    
    def store_bets_per_agency(self, agency_id, bets):
        for bet in bets:
            self.agencies[agency_id].bets[int(bet.document)] = bet
    
    def check_finished(self):
        if self.amount_of_agencies_ready != self.amount_of_agencies:
            return False
        for bet in load_bets():
            if not has_won(bet):
                continue
            document = int(bet.document)
            logging.info(
                f"actual_bet: {bet}"
            )
            logging.info(
                f"agencies_state: {self.agencies}"
            )
            for agency in self.agencies.values():

                if agency.bets[document]:
                    agency.winners.append(document)
        return True
    
    def get_winners_of_agency(self, agency_number):
        return self.agencies[agency_number].winners
