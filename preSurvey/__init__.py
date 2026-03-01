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
    # 人間意思決定预测
    p1_stage1_offer = models.IntegerField(
        min=0, max=100,
        label='本日の参加者がP1として行動する時、ステージ1で相手に提示するポイント数の平均値を予測してください'
    )
    p2_stage2_offer = models.IntegerField(
        min=0, max=100,
        label='本日の参加者がP2として行動する時、ステージ2で相手に提示するポイント数の平均値を予測してください'
    )
    p1_stage3_offer = models.IntegerField(
        min=0, max=100,
        label='本日の参加者がP1として行動する時、ステージ3で相手に提示するポイント数の平均値を予測してください'
    )

    AveStage = models.FloatField(
        min=1.0, max=3.0,
        label='本日の参加者が平均して到達するステージ数を予測してください（1.0〜3.0の数値で入力,小数可）'
    )

    # 基本偏好
    acceptable_minimum = models.IntegerField(
        min=0, max=100,
        label='あなたが受け入れ可能な最小のポイント数はいくつですか？'
    )

    svo_question = models.IntegerField(
        min=1, max=3,
        label='以下のうち、あなたの考えに最も近いものはどれですか？',
        choices=[
            [1, '自分の利益を最大化することが最も重要'],
            [2, '自分と相手の合計利益を最大化することが最も重要'],
            [3, '自分と相手の利益の差を最小化することが最も重要（公平性）']
        ]
    )

    # AI行動預測、t２、t３のみ
    AI_stage1_offer = models.IntegerField(
        min=0, max=100,
        blank=True,  # T1では入力不要
        label='AIがP1として行動する時、ステージ1で相手に提示するポイント数の平均値を予測してください'
    )
    AI_stage2_offer = models.IntegerField(
        min=0, max=100,
        blank=True,
        label='AIがP2として行動する時、ステージ2で相手に提示するポイント数の平均値を予測してください'
    )
    AI_stage3_offer = models.IntegerField(
        min=0, max=100,
        blank=True,
        label='AIがP1として行動する時、ステージ3で相手に提示するポイント数の平均値を予測してください'
    )

    AI_competitiveness = models.IntegerField(
        min=1, max=7,
        blank=True,
        label='AIはどの程度競争的だと思いますか？（1〜7の整数で回答、1=非常に協力的、7=非常に競争的）'
    )

    ai_trustworthiness = models.IntegerField(
        min=1, max=7,
        blank=True,
        null=True,
        label='AIをどの程度信頼できると思いますか？（1〜7の整数、1=全く信頼できない、7=非常に信頼できる）'
    )

    ai_predictability = models.IntegerField(
        min=1, max=7,
        blank=True,
        null=True,
        label='AIの行動はどの程度予測可能だと思いますか？（1〜7の整数、1=全く予測できない、7=非常に予測可能）'
    )


# PAGES
class PriorQ(Page):
    form_model = 'player'
    if Treatment == 1:
        form_fields = ['p1_stage1_offer','p2_stage2_offer','p1_stage3_offer','AveStage','acceptable_minimum','svo_question']
    else:
        form_fields = ['p1_stage1_offer','p2_stage2_offer','p1_stage3_offer','AveStage','acceptable_minimum','svo_question','AI_stage1_offer','AI_stage2_offer','AI_stage3_offer','AI_competitiveness','ai_trustworthiness','ai_predictability']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
         Treatment = Treatment
        )

class Waitpage(WaitPage):
    pass

class GotoMainTask(Page):
    timeout_seconds = 15


page_sequence = [PriorQ,Waitpage,GotoMainTask]
