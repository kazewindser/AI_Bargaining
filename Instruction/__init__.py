from otree.api import *
from settings import Treatment


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instruction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Waitplease(Page):
    pass

class Instruction(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Treatment = Treatment
    )



page_sequence = [Waitplease,Instruction]
