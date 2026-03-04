from otree.api import *
from otree.models import player

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
    if subsession.round_number == 1:  # 只在第1轮初始化
        for p in subsession.get_players():
            p.participant.ROLE = []
            p.participant.Discounted_points_Per_Round = []
            p.participant.PairedLabel = []

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

    potential_point = models.IntegerField(initial=0,min=0,max=100)

    discount_rate = models.FloatField(initial=1,min=0,max=1)
    Discounted_points = models.FloatField(initial=0,min=0,max=100)

    accepted_offer = models.BooleanField(
        choices=[[True, '受け入れる / Accept'], [False, '拒否する / Reject']],
        widget=widgets.RadioSelect,
        blank=True,
        label="あなたの選択"
    )


class BargainingLog(ExtraModel):
    player = models.Link(Player)
    stage = models.IntegerField(initial=1, min=1, max=4)
    offer_to_other = models.IntegerField(null=True)
    offer_from_other = models.IntegerField(null=True)
    accepted = models.BooleanField(null=True)
    Role = models.StringField(null=True)


def custom_export(players):
    yield ['session','participant_code', 'participant_label', 'round_number', 'stage', 'role', 'offer_to_other',
           'offer_from_other', 'accepted']

    LOGS = BargainingLog.filter()
    for log in LOGS:
        player = log.player
        participant = player.participant
        session = player.session
        yield [session.code, participant.code, participant.label, player.round_number, log.stage, log.Role, log.offer_to_other, log.offer_from_other, log.accepted]


def SaveQ(subsession):
    # 先保存配对信息
    for group in subsession.get_groups():
        for p in group.get_players():
            p.participant.PairedLabel.append(p.get_others_in_group()[0].participant.label)

    for p in subsession.get_players():
        p.participant.ROLE.append(p.role)
        p.participant.Discounted_points_Per_Round.append(p.Discounted_points)




# PAGES

class Title(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

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
            BargainingLog.create(player=player,stage=player.group.group_stage,Role=player.role,offer_to_other=data['value'], accepted=None)
            player.potential_point = 100-data['value']
            Pother.potential_point = data['value']
            # 发送offer给对方
            response[Pother.id_in_group] = {
                'otherOffer': data['value'],
                'group_stage': player.group.group_stage,
            }
            # 通知发送方对方正在考虑
            response[player.id_in_group] = {
                'otherIsConsidering': True,
            }
        elif data['type'] == 'acceptance':
            # Convert string 'True'/'False' to boolean if needed
            accepted_value = data['value']
            if isinstance(accepted_value, str):
                accepted_value = data['value'] == 'True'
            BargainingLog.create(player=player, stage=player.group.group_stage, Role=player.role,offer_from_other=player.potential_point, accepted=accepted_value)
            if accepted_value:
                player.group.game_finished = True
                player.Discounted_points = round(player.potential_point * player.discount_rate,2)
                Pother.Discounted_points = round(Pother.potential_point * Pother.discount_rate,2)
            else:
                player.group.group_stage += 1
                if player.group.group_stage >= 4:
                    player.group.game_finished = True
                    player.Discounted_points = 0
                    Pother.Discounted_points = 0
                else:
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
    timeout_seconds = 10
    pass

class WaitForNext(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        SaveQ(subsession)
        subsession.group_randomly()

page_sequence = [Title,Bargaining,Results,WaitForNext]


