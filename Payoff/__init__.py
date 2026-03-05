from otree.api import *
from settings import Treatment
import math


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'PayoffT1T2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

def ceil_to_10(x: float) -> int:
    return int(math.ceil(x / 10) * 10)


# PAGES
class FinalResults(Page):

    @staticmethod
    def vars_for_template(player):
        selectedRound = player.participant.SelectedRound
        final_point_payoff = player.participant.Final_Point_Payoff
        ROLE = player.participant.ROLE
        Discounted_points_Per_Round = player.participant.Discounted_points_Per_Round
        selectedROLE= ROLE[selectedRound-1]
        AddPayoff = ceil_to_10(final_point_payoff * 40)

        # Zip ROLE and Discounted_points_Per_Round for template iteration
        round_data = list(zip(ROLE, Discounted_points_Per_Round))

        #for T3
        if Treatment == 3:
            id_sameAIpoints = player.participant.id_sameAIpoints
            T3_whether_getAI_OFFER = player.participant.T3_whether_getAI_OFFER
            if T3_whether_getAI_OFFER:
                if selectedROLE == 'P1':
                    sameAIpoints = player.participant.T3_AI_P1_Discounted_points[selectedRound]
                else:
                    sameAIpoints = player.participant.T3_AI_P2_Discounted_points[selectedRound]
            else:
                sameAIpoints = []
        else:
            id_sameAIpoints = -1
            T3_whether_getAI_OFFER = False
            sameAIpoints = []

        return dict(
            selectedRound = selectedRound,
            final_point_payoff = final_point_payoff,
            round_data = round_data,
            selectedROLE = selectedROLE,
            AddPayoff = AddPayoff,
            Treatment = Treatment,

            id_sameAIpoints = id_sameAIpoints,
            T3_whether_getAI_OFFER = T3_whether_getAI_OFFER,
            sameAIpoints = sameAIpoints,
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinalResults]
