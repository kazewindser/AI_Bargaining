from otree.api import *
import random


#### AI setting #################
from openai import OpenAI
from pydantic import BaseModel, Field
import os

from .Prompts import SYSTEM_PROMPT,user_prompt_P1_stage1_initial
client = OpenAI(api_key=os.environ.get('AI_Bargaining_KEY'))


MODEL = "gpt-5.2"
TEMP = 1

class P1_stage1_initial(BaseModel):
    # AI作为p1一开始的offer
    Offer_to_P2_stage1: int = Field(ge=0, le=100)

class P1_stage2_stage3(BaseModel):
    # AI作为P1在stage2要不要接受或者拒绝进入stage3
    Whether_to_accept_P2_offer_stage2: bool
    Offer_to_P2_if_rejected_proceed_to_stage3: int

class P2_stage1_stage2(BaseModel):
    # AI作为P2在stage1要不要接受或者拒绝进入stage2
    Whether_to_accept_P1_offer_stage1: bool
    Offer_to_P1_if_rejected_proceed_to_stage2: int

class P2_stage3_end(BaseModel):
    # AI作为P2在stage3要不要接受或者拒绝然后结束
    Whether_to_accept_P1_offer_stage3: bool

def ElicitAIResp_P1_stage1_initial():
    response = client.responses.parse(
        model=MODEL,
        input=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": user_prompt_P1_stage1_initial}
        ],
        temperature=TEMP,
        text_format=P1_stage1_initial,
    )
    response_content = response.output_parsed
    prediction_dict = response_content.model_dump()
    print(prediction_dict)
    return int(prediction_dict["Offer_to_P2_stage1"])

def ElicitAIResp_P2_stage1_stage2(player):
    HumanP1toAIP2stage1 = player.HumanP1toAIP2stage1
    user_prompt_P2_stage1_stage2 = f"""
    Follow the game rules defined in the system prompt.
    -Role: P2
    -The human player is P1.
    -Current Stage: 1
    -P1 has decided to propose {HumanP1toAIP2stage1} points to you.

    -Decision required:
    1. Decide whether to ACCEPT this offer: Whether_to_accept_P1_offer_stage1: <TRUE/FALSE>
    2. If you REJECT, propose an offer for Stage 2: Offer_to_P1_if_rejected_proceed_to_stage2: <integer or -1 if accepted>
    """
    print(user_prompt_P2_stage1_stage2)
    response = client.responses.parse(
        model=MODEL,
        input=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": user_prompt_P2_stage1_stage2}
        ],
        temperature=TEMP,
        text_format=P2_stage1_stage2,
    )
    response_content = response.output_parsed
    prediction_dict = response_content.model_dump()
    print(prediction_dict)
    return prediction_dict

def ElicitAIResp_P2_stage3_end(player):
    HumanP1toAIP2stage1 = player.HumanP1toAIP2stage1
    AIP2toHumanP1stage2 = player.AIP2toHumanP1stage2
    HumanP1toAIP2stage3 = player.HumanP1toAIP2stage3

    user_prompt_P2_stage3_end = f"""
    Follow the game rules defined in the system prompt.
    Role: P2
    The human player is P1.

    Current Stage: 3
    -History:
    -Stage 1: P1 proposed {HumanP1toAIP2stage1} points to you. You rejected the offer.
    -Stage 2: You proposed {AIP2toHumanP1stage2} points to P1. P1 rejected the offer.
    -Stage 3: P1 now proposes {HumanP1toAIP2stage3} points to you.

    -Decision required:
    Decide whether to accept the offer: Whether_to_accept_P1_offer_stage3: <TRUE/FALSE>
    """
    response = client.responses.parse(
        model=MODEL,
        input=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": user_prompt_P2_stage3_end}
        ],
        temperature=TEMP,
        text_format=P2_stage3_end,
    )
    response_content = response.output_parsed
    prediction_dict = response_content.model_dump()
    print(prediction_dict)
    return prediction_dict

def ElicitAIResp_P1_stage2_stage3(player):
    AIP1toHumanP2stage1 = player.AIP1toHumanP2stage1
    HumanP2toAIP1stage2 = player.HumanP2toAIP1stage2
    user_prompt_P1_stage2_stage3 = f"""
    Follow the game rules defined in the system prompt.
    -Role: P1
    -The human player is P2.
    -Current Stage: 2
    -Stage 1 history:
    You proposed {AIP1toHumanP2stage1} points to P2.
    P2 rejected the offer.

    -Stage 2: P2 has decided to propose {HumanP2toAIP1stage2} points to you.

    -Decision required:
    1. Decide whether to ACCEPT this offer: Whether_to_accept_P2_offer_stage2: <TRUE/FALSE>
    2. If you REJECT, propose an offer (0–100) to P2 for Stage 3: Offer_to_P2_if_rejected_proceed_to_stage3: <integer or -1 if accepted>
    """

    response = client.responses.parse(
        model=MODEL,
        input=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": user_prompt_P1_stage2_stage3}
        ],
        temperature=TEMP,
        text_format=P1_stage2_stage3,
    )
    response_content = response.output_parsed
    prediction_dict = response_content.model_dump()
    print(prediction_dict)
    return prediction_dict


####################################


doc = """
Bargaining with AI
"""


class C(BaseConstants):
    NAME_IN_URL = 'AI_BNF'
    PLAYERS_PER_GROUP = None
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

    players = subsession.get_players()
    random.shuffle(players)

    half = len(players) // 2
    for i, p in enumerate(players):
        p.Role = 'P1' if i < half else 'P2'
    if len(players) % 2:
        players[-1].Role = random.choice(['P1', 'P2'])

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    CurrentStage = models.IntegerField(initial=1, min=1, max=4)

    offer_points = models.IntegerField(min=0,max=100,blank=True,label="応答者に提案する点数（0-100）")
    accepted_offer = models.BooleanField(choices=[[True, '受け入れる / Accept'], [False, '拒否する / Reject']],widget=widgets.RadioSelect,
        blank=True,label="あなたの選択"
    )

    Role = models.StringField()

    potential_point = models.IntegerField(initial=0,min=0,max=100)
    discount_rate = models.FloatField(initial=1,min=0,max=1)
    AIdiscount_rate = models.FloatField(initial=1,min=0,max=1)
    Discounted_points = models.FloatField(initial=0,min=0,max=100)
    AIdiscounted_points = models.FloatField(initial=0,min=0,max=100)

    #LOGOFFER (AIP1;HumanP2)
    AIP1toHumanP2stage1 = models.IntegerField(initial=-2,max=100)
    HumanP2toAIP1stage2 = models.IntegerField(initial=-2,max=100)
    AIP1toHumanP2stage3 = models.IntegerField(initial=-2,max=100)

    # LOGOFFER (HumanP1;AIP2)
    HumanP1toAIP2stage1 = models.IntegerField(initial=-2,max=100)
    AIP2toHumanP1stage2 = models.IntegerField(initial=-2,max=100)
    HumanP1toAIP2stage3 = models.IntegerField(initial=-2,max=100)

    game_finished = models.BooleanField(initial=False)
    accepted_at_stage = models.IntegerField(initial=0,min=0,max=4)


class BargainingLog(ExtraModel):
    player = models.Link(Player)
    stage = models.IntegerField(initial=1, min=1, max=4)
    offer_to_AI = models.IntegerField(null=True)
    offer_from_AI = models.IntegerField(null=True)
    accepted = models.BooleanField(null=True)
    Role = models.StringField(null=True)



def SaveQ(subsession):
    for p in subsession.get_players():
        p.participant.ROLE.append(p.Role)
        p.participant.Discounted_points_Per_Round.append(p.Discounted_points)

def custom_export(players):
    # header row
    yield ['session', 'participant_code', 'label',
           'Role','CurrentStage','Accepted_at_stage',
           'AIP1toHumanP2stage1','HumanP2toAIP1stage2','AIP1toHumanP2stage3',
           'HumanP1toAIP2stage1','AIP2toHumanP1stage2','HumanP1toAIP2stage3',
           'FinalDiscounted_points','FinalAIdiscounted_points'
           ]
    for p in players:
        participant = p.participant
        session = p.session
        yield [
        session.code, participant.code, participant.label,
        p.Role, p.CurrentStage, p.accepted_at_stage,
        p.AIP1toHumanP2stage1, p.HumanP2toAIP1stage2, p.AIP1toHumanP2stage3,
        p.HumanP1toAIP2stage1, p.AIP2toHumanP1stage2, p.HumanP1toAIP2stage3,
        p.Discounted_points, p.AIdiscounted_points
        ]



# PAGES
class Title(Page):
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class AI_Bargaining(Page):
    form_model = 'player'
    form_fields = ['offer_points','accepted_offer']

    @staticmethod
    def vars_for_template(player):
        discount_rate =  player.discount_rate
        AI_role = 'P1' if player.Role == 'P2' else 'P2'
        if player.Role == 'P2':
            player.AIP1toHumanP2stage1 = ElicitAIResp_P1_stage1_initial()
            player.potential_point = player.AIP1toHumanP2stage1
        AIP1toHumanP2stage1 = player.AIP1toHumanP2stage1
        return dict(
            CurrentStage = player.CurrentStage,
            discount_rate = discount_rate,
            AI_role = AI_role,
            AIP1toHumanP2stage1 = AIP1toHumanP2stage1,
        )

    @staticmethod
    def live_method(player, data):
        response = {}

        if data['type'] == 'offer':
            if player.Role == 'P1':
                if player.CurrentStage == 1:
                    player.HumanP1toAIP2stage1 = data['value']
                    player.potential_point = 100-player.HumanP1toAIP2stage1
                    AIP2stage1Resp = ElicitAIResp_P2_stage1_stage2(player)
                    Accepted = AIP2stage1Resp['Whether_to_accept_P1_offer_stage1']
                    OfferifRejected = AIP2stage1Resp['Offer_to_P1_if_rejected_proceed_to_stage2']
                    if Accepted:
                        player.Discounted_points = round(player.potential_point * player.discount_rate, 2)
                        player.AIdiscounted_points = round((100-player.potential_point) * player.AIdiscount_rate, 2)
                        player.game_finished = True
                        player.accepted_at_stage = player.CurrentStage
                    else:
                        player.potential_point = OfferifRejected
                        player.AIP2toHumanP1stage2 = OfferifRejected
                        player.CurrentStage += 1
                        player.discount_rate *= 0.6
                        player.AIdiscount_rate *= 0.4
                        print('Offer_to_P1_if_rejected_proceed_to_stage2:', OfferifRejected)

                    response[player.id_in_group] = {
                        'game_finished': player.game_finished,
                        'AIaccept': Accepted,
                        'AIOffer': OfferifRejected,
                        'Current_discount_rate': player.discount_rate,
                        'CurrentStage': player.CurrentStage,
                        }
                if player.CurrentStage == 3:
                    player.HumanP1toAIP2stage3 = data['value']
                    player.potential_point = 100 - player.HumanP1toAIP2stage3
                    AIP2stage3Resp = ElicitAIResp_P2_stage3_end(player)
                    Accepted = AIP2stage3Resp['Whether_to_accept_P1_offer_stage3']
                    if Accepted:
                        player.Discounted_points = round(player.potential_point * player.discount_rate, 2)
                        player.AIdiscounted_points = round((100-player.potential_point) * player.AIdiscount_rate, 2)
                        player.accepted_at_stage = player.CurrentStage
                    else:
                        player.Discounted_points = 0
                        player.AIdiscounted_points = 0
                        player.accepted_at_stage = player.CurrentStage+1
                        #不管怎么说都结束了
                    player.game_finished = True


                    response[player.id_in_group] = {
                        'game_finished': player.game_finished,
                        'AIaccept': Accepted,
                    }

            if player.Role == 'P2':
                if player.CurrentStage == 2:
                    player.HumanP2toAIP1stage2 = data['value']
                    player.potential_point = 100 - player.HumanP2toAIP1stage2
                    AIP1stage2Resp = ElicitAIResp_P1_stage2_stage3(player)
                    Accepted = AIP1stage2Resp['Whether_to_accept_P2_offer_stage2']
                    OfferifRejected = AIP1stage2Resp['Offer_to_P2_if_rejected_proceed_to_stage3']
                    player.AIP1toHumanP2stage3 = OfferifRejected
                    print('Offer_to_P2_if_rejected_proceed_to_stage3:', OfferifRejected)
                    print('Accepted:', Accepted)
                    if Accepted:
                        player.Discounted_points = round(player.potential_point * player.discount_rate, 2)
                        player.AIdiscounted_points = round((100-player.potential_point) * player.AIdiscount_rate, 2)
                        player.game_finished = True
                        player.accepted_at_stage = player.CurrentStage
                    else:
                        player.potential_point = OfferifRejected
                        player.CurrentStage += 1
                        player.discount_rate *= 0.4
                        player.AIdiscount_rate *= 0.6

                    response[player.id_in_group] = {
                        'game_finished': player.game_finished,
                        'AIaccept': Accepted,
                        'AIOffer': OfferifRejected,
                        'Current_discount_rate': player.discount_rate,
                        'CurrentStage': player.CurrentStage,
                    }

        elif data['type'] == 'acceptance':
            # Convert string 'True'/'False' to boolean if needed
            accepted_value = data['value']
            if isinstance(accepted_value, str):
                accepted_value = data['value'] == 'True'
                if accepted_value:
                    player.game_finished = True
                    player.accepted_at_stage = player.CurrentStage
                    player.Discounted_points = round(player.potential_point * player.discount_rate, 2)
                    player.AIdiscounted_points = round((100-player.potential_point) * player.AIdiscount_rate, 2)
                else:
                    player.CurrentStage += 1
                    if player.CurrentStage >= 4:
                        player.game_finished = True
                        player.accepted_at_stage = player.CurrentStage
                        player.Discounted_points = 0
                        player.AIdiscounted_points = 0
                    else:
                        player.discount_rate *= C.DISCOUNT_P1 if player.Role == C.P1_ROLE else C.DISCOUNT_P2
                        player.AIdiscount_rate *= C.DISCOUNT_P2 if player.Role == C.P1_ROLE else C.DISCOUNT_P1
                    
                    
            response[player.id_in_group] = {
                'game_finished': player.game_finished,
                'CurrentStage': player.CurrentStage,
                'Current_discount_rate': player.discount_rate,
                'AIdiscount_rate': player.AIdiscount_rate,
            }
        return response

    @staticmethod
    def js_vars(player):
        return dict(
            payoff=player.payoff,
        )


class Results(Page):
    timeout_seconds = 10
    pass

class WaitForNext(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        SaveQ(subsession)

page_sequence = [Title,AI_Bargaining,Results,WaitForNext]
