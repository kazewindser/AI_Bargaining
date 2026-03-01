from otree.api import *
from settings import Treatment

doc = """
実験クイズアプリ - 6問の理解度確認テスト
"""


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6

    if Treatment == 1:
        QUESTIONS = [
            {
                'question': '本実験は合計10ラウンドで実施されます。各ラウンドには必ず3つのステージがあります。',
                'choices': [
                    [1, 'はい'],
                    [2, 'いいえ']
                ],
                'correct': 2,
                'error_msg': '残念ですが、不正解です。各ラウンドには最大で3つのステージがあります。ステージ1とステージ2のオファーがいずれも拒否された場合にのみ、ステージ3が実施されます。'
            },
            {
                'question': 'あなたがP2のとき、ステージ2では、あなたがP1にオファーを出しますか？',
                'choices': [
                    [1, 'はい'],
                    [2, 'いいえ']
                ],
                'correct': 1,
                'error_msg': '残念ですが、不正解です。P2はステージ2でP1にオファーを出します。ステージ1とステージ3では、P1からのオファーを受け入れるかどうかを決定します。'
            },
            {
                'question': 'あなたがP1のとき、ステージ2でP2があなたに50ポイントを提案しました。提案を受け入れた場合、割引後にあなたが最終的に得るポイントはいくつですか？',
                'choices': [
                    [1, '0'],
                    [2, '10'],
                    [3, '20'],
                    [4, '30']
                ],
                'correct': 4,
                'error_msg': '残念ですが、不正解です。P1のステージ2における割引率は0.6です。'
            },
            {
                'question': 'あなたがP2のとき、ステージ3でP1があなたに40ポイントを提案しました。提案を受け入れた場合、割引後にあなたが最終的に得るポイントはいくつですか？',
                'choices': [
                    [1, '0'],
                    [2, '8'],
                    [3, '16'],
                    [4, '40']
                ],
                'correct': 2,
                'error_msg': '残念ですが、不正解です。P2のステージ3における割引率は0.16です。'
            },
            {
                'question': 'あなたがP2のとき、ステージ3でP1があなたに50ポイントを提案しました。提案を拒否した場合、割引後にあなたが最終的に得るポイントはいくつですか？',
                'choices': [
                    [1, '0'],
                    [2, '8'],
                    [3, '16'],
                    [4, '40']
                ],
                'correct': 1,
                'error_msg': '残念ですが、不正解です。ステージ3でオファーが拒否された場合、P1とP2の得点はどちらも0になります。その時点でゲームは自動的に終了します。'
            },
            {
                'question': '参加費以外の追加報酬は各ラウンドであなた自身が獲得したポイントPに関わり、総追加報酬はすべてのラウンドの報酬の合計です。',
                'choices': [
                    [1, 'はい'],
                    [2, 'いいえ']
                ],
                'correct': 2,
                'error_msg': '残念ですが、不正解です。追加報酬Bは、全ラウンドの中からランダムに1ラウンドが選ばれ、そのラウンドであなたが獲得したポイントに基づいて決定されます。'
            },
        ]
    elif Treatment == 2:
        QUESTIONS = [
            {
                'question': '本実���では、合計で何ラウンド実施されますか？',
                'choices': [
                    [1, '1'],
                    [2, '4'],
                    [3, '8'],
                    [4, '10']
                ],
            }
        ]
    else:
        QUESTIONS = [
            {
                'question': '本実���では、合計で何ラウンド実施されますか？',
                'choices': [
                    [1, '1'],
                    [2, '4'],
                    [3, '8'],
                    [4, '10']
                ],
            }
        ]




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