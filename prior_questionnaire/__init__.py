from otree.api import *
from preSurvey._lexicon_q import Lexicon

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'prior_questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    AIorHUMAN = models.IntegerField(
        label = Lexicon.q_AIorHUMAN,
        choices = Lexicon.q_AIorHUMAN_opts
    )

    predict_accu1 = models.IntegerField(min=0, max=100)
    predict_accu2 = models.IntegerField(min=0, max=100)

    AI_accuracy = models.IntegerField(min=0, max=100)
    Human_accuracy = models.IntegerField(min=0, max=100)
    Human_accuracy2 = models.IntegerField(min=0, max=100)

    AveWTP1 = models.IntegerField(min=0, max=500)
    AveWTP2 = models.IntegerField(min=0, max=500)




# PAGES
# def custom_export(players):
#     # header row
#     yield ['session', 'participant_code', 'label',  'id_in_group',
#    'AIorHUMAN']
#     for p in players:
#         participant = p.participant
#         session = p.session
#         yield [
#         session.code, participant.code, participant.label,  p.id_in_group, 
#         p.AIorHUMAN
#         ]      


class PriorQ(Page):
    form_model = 'player'
    form_fields = ['AIorHUMAN','predict_accu1','predict_accu2','AI_accuracy','Human_accuracy','Human_accuracy2','AveWTP1','AveWTP2']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
        )
class Waitpage(WaitPage):
    pass

class GotoMainTask(Page):
    timeout_seconds = 15
    




page_sequence = [PriorQ,Waitpage,GotoMainTask]
