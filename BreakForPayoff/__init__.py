from otree.api import *
from wtforms.validators import length
from settings import Treatment


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
    # Assigns random round and treatment-specific payoffs to group players
    for p in group.get_players():
        id_sameAIpoints = -2
        p.participant.id_sameAIpoints = id_sameAIpoints

        p.selectedRound = random.randint(1,10)
        p.participant.SelectedRound = p.selectedRound

        sameAIpoints = []

        if Treatment in (1, 2):
            p.final_point_payoff = p.participant.Discounted_points_Per_Round[p.selectedRound-1]
            p.payoff = ceil_to_10( p.final_point_payoff*40 )
            p.participant.T3_whether_getAI_OFFER = p.T3_whether_getAI_OFFER
        else:
            p.T3_whether_getAI_OFFER = random.choice([True, False])
            p.participant.T3_whether_getAI_OFFER = p.T3_whether_getAI_OFFER
            if p.T3_whether_getAI_OFFER:
                if p.participant.ROLE[p.selectedRound-1] == 'P1':
                    sameAIpoints = p.participant.T3_AI_P1_Discounted_points[p.selectedRound]
                else:
                    sameAIpoints = p.participant.T3_AI_P2_Discounted_points[p.selectedRound]

                id_sameAIpoints = random.choice(range(len(sameAIpoints)))
                p.participant.id_sameAIpoints = id_sameAIpoints
                p.final_point_payoff = sameAIpoints[id_sameAIpoints]
                p.payoff = ceil_to_10(p.final_point_payoff * 40)
            else:
                id_sameAIpoints = -1
                p.participant.id_sameAIpoints = id_sameAIpoints
                p.final_point_payoff = p.participant.Discounted_points_Per_Round[p.selectedRound-1]
                p.payoff = ceil_to_10(p.final_point_payoff * 40)
        p.participant.Final_Point_Payoff = p.final_point_payoff

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
    @staticmethod
    def vars_for_template(player):

        return dict(
            Treatment = Treatment,
        )


class ResultsWaitPage(WaitPage):
    pass



page_sequence = [Waitplease,Break, ResultsWaitPage]
