from otree.api import *

from preSurvey._lexicon_q import Lexicon
from settings import Treatment


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'preSurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


#预测今天参与者整体在每一轮的第一个stage给出的offer的平均
#预测今天参与者整体在每一轮的第二个stage（如果有）给出的offer的平均
#预测今天参与者整体在每一轮的第三个stage（如果有）给出的offer的平均
#预测今天实验的参与者平均到达stage数字(请给出一个大于1的小数)

#预测AI在每一轮的第一个stage给出的offer的平均
#预测AI在每一轮的第二个stage（如果有）给出的offer的平均
#预测AI在每一轮的第三个stage（如果有）给出的offer的平均



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    p1_stage1_offer = models.IntegerField(min=0, max=100)
    p2_stage2_offer = models.IntegerField(min=0, max=100)
    p1_stage3_offer = models.IntegerField(min=0, max=100)

    AveStage = models.FloatField(min=1, max=3)

    AI_stage1_offer = models.IntegerField(min=0, max=100)
    AI_stage2_offer = models.IntegerField(min=0, max=100)
    AI_stage3_offer = models.IntegerField(min=0, max=100)


# PAGES
class PriorQ(Page):
    form_model = 'player'
    if Treatment == 1:
        form_fields = ['p1_stage1_offer','p2_stage2_offer','p1_stage3_offer','AveStage','AI_stage1_offer','AI_stage2_offer','AI_stage3_offer']
    else:
        form_fields = ['p1_stage1_offer','p2_stage2_offer','p1_stage3_offer','AveStage']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
         Treatment = Treatment
        )
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
        )
class Waitpage(WaitPage):
    pass

class GotoMainTask(Page):
    timeout_seconds = 15


page_sequence = [MyPage, ResultsWaitPage, Results]
