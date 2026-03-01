from otree.api import *
from settings import Treatment
from Quiz.QuestionBank import *

doc = """
実験クイズアプリ - 6問の理解度確認テスト
"""


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8

    if Treatment == 3:
        QUESTIONS = T3_quiz
    else:
        QUESTIONS = T1_2quiz




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer = models.IntegerField()


class Start(Page):
    @staticmethod
    def is_displayed(p: Player):
        # 只在最后一轮显示
        return p.round_number == 1


class QuestionPage(Page):
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player: Player):
        question_data = C.QUESTIONS[player.round_number - 1]
        return {
            'question_num': player.round_number,
            'question_text': question_data['question'],
            'choices': question_data['choices'],
        }

    @staticmethod
    def error_message(player: Player, values):
        question_data = C.QUESTIONS[player.round_number - 1]
        if values['answer'] != question_data['correct']:
            return question_data['error_msg']


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class WaitForPlayers(WaitPage):
    """等待所有玩家完成所有轮次后再显示最终结果"""

    title_text = "お待ちください"
    body_text = "全ての参加者がクイズを終了するのを待ってください..."
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(p: Player):
        # 只在最后一轮显示
        return p.round_number == C.NUM_ROUNDS

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        pass


page_sequence = [Start,QuestionPage, Results, WaitForPlayers]