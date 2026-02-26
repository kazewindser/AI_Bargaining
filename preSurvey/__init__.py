from otree.api import *


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
#预测今天参与者整体在每一轮的第二个stage（如果有）给出的offer的平均
#预测今天参与者整体在每一轮的第三个stage（如果有）给出的offer的平均



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
