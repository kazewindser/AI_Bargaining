from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Human'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2

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
    game_finished = models.BooleanField(initial=False)
    group_stage = models.IntegerField(min=1,max=4,initial=1)


class Player(BasePlayer):
    ReachStage = models.IntegerField(initial=1, min=1, max=4)

    offer_points = models.IntegerField(
        min=0,
        max=100,
        blank=True,
        label="応答者に提案する点数（0-100）"
    )

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

    accepted_offer = models.BooleanField(
        choices=[[True, '受け入れる / Accept'], [False, '拒否する / Reject']],
        widget=widgets.RadioSelect,
        blank=True,
        label="あなたの選択"
    )


class BargainingLog(ExtraModel):
    player = models.Link(Player)
    group = models.Link(Group)
    stage = models.IntegerField(initial=1, min=1, max=4)
    offer = models.IntegerField(null=True)
    accepted = models.BooleanField(null=True)

def custom_export(players):
    # header row
    yield ['label', 'round_number','stage','role','offer']

    # 'filter' without any args returns everything
    LOGS = BargainingLog.filter()
    for log in LOGS:
        player = LOGS.player
        yield [player.label, player.round_number, log.stage, player.role, log.offer,log.accepted]




# PAGES
class Bargaining(Page):
    form_model = 'player'
    form_fields = ['offer_points','accepted_offer']

    @staticmethod
    def vars_for_template(player):
        discount_rate =  player.discount_rate
        ReachStage = player.ReachStage
        other_role= player.get_others_in_group()[0]
        return dict(
            discount_rate = discount_rate,
            ReachStage = ReachStage,
            other_role = other_role.role
        )

    @staticmethod
    def live_method(player, data):
        response = {}
        Pother = player.get_others_in_group()[0]

        if data['type'] == 'offer':
            BargainingLog.create(player=player, stage=player.group.group_stage, offer=data['value'], accepted=None)
            # P1发送offer给P2
            response[Pother.id_in_group] = {
                'otherOffer': data['value'],
                'group_stage': player.group.group_stage,
            }
        elif data['type'] == 'acceptance':
            # Convert string 'True'/'False' to boolean if needed
            accepted_value = data['value']
            if isinstance(accepted_value, str):
                accepted_value = data['value'] == 'True'
            BargainingLog.create(player=player, stage=player.group.group_stage, offer=None, accepted=accepted_value)
            if accepted_value:
                player.group.game_finished = True
            else:
                player.group.group_stage += 1
                if player.group.group_stage == 4:
                    player.group.game_finished = True

                for p in [player, Pother]:
                    p.discount_rate *= C.DISCOUNT_P1 if p.role == C.P1_ROLE else C.DISCOUNT_P2

            response[Pother.id_in_group] = {
                'otherAcceptance': accepted_value,
                'game_finished': player.group.game_finished,
                'group_stage': player.group.group_stage,
                'discount_rate': Pother.discount_rate,
            }

            response[player.id_in_group] = {
                'game_finished': player.group.game_finished,
                'group_stage': player.group.group_stage,
                'discount_rate': player.discount_rate,
            }

        return response

class Results(Page):
    pass

class ResultsWaitPage(WaitPage):
    pass




page_sequence = [Bargaining, ResultsWaitPage, Results]
