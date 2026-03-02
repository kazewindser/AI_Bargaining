from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Human'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10

    P1_ROLE = 'P1'
    P2_ROLE = 'P2'

    # 折扣率设置
    DISCOUNT_P1 = 0.6  # P1每阶段的折扣率
    DISCOUNT_P2 = 0.4  # P2每阶段的折扣率




class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    subsession.group_randomly()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ReachStage = models.IntegerField(initial=1, min=1, max=4)

    # Serve As P1
    Stage1_P1propose_toP2 = models.IntegerField(initial=-1,min=0,max=100)
    Stage2_P1offer_fromP2 = models.IntegerField(initial=-1,min=0,max=100)
    Stage3_P1propose_toP2 = models.IntegerField(initial=-1,min=0,max=100)


    # Serve As P2
    Stage1_P2offer_fromP1 = models.IntegerField(initial=-1,min=0,max=100)
    Stage2_P2propose_toP1 = models.IntegerField(initial=-1,min=0,max=100)
    Stage3_P2offer_fromP1 = models.IntegerField(initial=-1,min=0,max=100)

    discount_rate = models.FloatField(initial=1,min=0,max=1)
    Success = models.BooleanField(initial=False)
    Discounted_points = models.FloatField(initial=0,min=0,max=100)

class BargainingLog(ExtraModel):
    player = models.Link(Player)
    group = models.Link(Group)
    round_number = models.IntegerField()
    stage = models.IntegerField()
    role = models.StringField()   # 'P1' or 'P2'
    action_type = models.StringField()  # 'propose' or 'accept'
    offer = models.IntegerField(null=True)
    accepted = models.BooleanField(null=True)


# PAGES
class Bargaining(Page):



    @staticmethod
    def vars_for_template(player):
        discount_rate =  player.discount_rate
        ReachStage = player.ReachStage
        return dict(
            discount_rate = discount_rate,
            ReachStage = ReachStage
        )

class Results(Page):
    pass

class ResultsWaitPage(WaitPage):
    pass




page_sequence = [Bargaining, ResultsWaitPage, Results]
