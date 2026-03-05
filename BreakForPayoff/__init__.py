from otree.api import *
from settings import Treatment
import math

import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Break'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    selectedRound = models.IntegerField(min=1, max=10)
    T3_whether_getAI_OFFER = models.BooleanField(initial=False)
    final_point_payoff = models.FloatField()

def ceil_to_10(x: float) -> int:
    return int(math.ceil(x / 10) * 10)

def set_payoffs(group):
    for p in group.get_players():

        p.selectedRound = random.randint(1,10)
        p.participant.SelectedRound = p.selectedRound

        if Treatment in (1, 2):
            p.final_point_payoff = p.participant.Discounted_points_Per_Round[p.selectedRound-1]
            p.payoff = ceil_to_10( p.final_point_payoff*40 )
        else:
            p.T3_whether_getAI_OFFER = random.randint(True, False)
            p.participant.T3_whether_getAI_OFFER = p.T3_whether_getAI_OFFER
            if p.T3_whether_getAI_OFFER:
                p.final_point_payoff = p.participant.Discounted_points_Per_Round[p.selectedRound-1]
                p.payoff = ceil_to_10(p.final_point_payoff * 40)
            else:
                p.final_point_payoff = p.participant.Discounted_points_Per_Round[p.selectedRound-1]
                p.payoff = ceil_to_10(p.final_point_payoff * 40)

def custom_export(players):
    # header row
    yield ['label', 'Final_Payoff']
    for p in players:
        participant = p.participant
        FINAL_PAYOFF = participant.payoff_plus_participation_fee()
        yield [
        participant.label, FINAL_PAYOFF
        ]




# PAGES
class Waitplease(WaitPage):
    after_all_players_arrive = set_payoffs

class Break(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass



page_sequence = [Waitplease,Break, ResultsWaitPage]
