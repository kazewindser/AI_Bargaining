from otree.api import *
from ._lexicon_q import *
from settings import Treatment

if Treatment == 1:
    Lexicon = LexiconHM
elif Treatment == 2:
    Lexicon = LexiconAI_T2T3
else:
    Lexicon = LexiconAI_T3

doc = """
questionnaire
"""

class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    age = models.IntegerField(
        min=17, max=100,
        label=Lexicon.q_age
    )
    gender = models.IntegerField(
        label=Lexicon.q_gender,
        choices=Lexicon.q_gender_opts
    )
    affiliate = models.IntegerField(
        label=Lexicon.q_affiliate,
        choices=Lexicon.q_affiliate_opts
    )

    consider_counterparty_payoff = models.IntegerField(
        label=getattr(Lexicon, "q_consider_counterparty_payoff", ""),
        choices=getattr(Lexicon, "q_consider_counterparty_payoff_opts", []),
    )
    anger_unfair_offer = models.IntegerField(
        label=getattr(Lexicon, "q_anger_unfair_offer", ""),
        choices=getattr(Lexicon, "q_anger_unfair_offer_opts", []),
    )
    chatgpt_use = models.IntegerField(
        label=getattr(Lexicon, "q_chatgpt_use", ""),
        choices=getattr(Lexicon, "q_chatgpt_use_opts", []),
    )
    chatgpt_frequency = models.IntegerField(
        label=getattr(Lexicon, "q_chatgpt_frequency", ""),
        choices=getattr(Lexicon, "q_chatgpt_frequency_opts", []),
    )

    knowing_ai_affected_decision = models.IntegerField(
        label=getattr(Lexicon, "q_knowing_ai_affected_decision", ""),
        choices=getattr(Lexicon, "q_knowing_ai_affected_decision_opts", []),
    )
    consider_ai_payoff = models.IntegerField(
        label=getattr(Lexicon, "q_consider_ai_payoff", ""),
        choices=getattr(Lexicon, "q_consider_ai_payoff_opts", []),
    )
    anger_unfair_ai_offer = models.IntegerField(
        label=getattr(Lexicon, "q_anger_unfair_ai_offer", ""),
        choices=getattr(Lexicon, "q_anger_unfair_ai_offer_opts", []),
    )
    felt_humanness_or_trust = models.IntegerField(
        label=getattr(Lexicon, "q_felt_humanness_or_trust", ""),
        choices=getattr(Lexicon, "q_felt_humanness_or_trust_opts", []),
    )

    knew_ai_score_may_affect_others = models.IntegerField(
        label=getattr(Lexicon, "q_knew_ai_score_may_affect_others", ""),
        choices=getattr(Lexicon, "q_knew_ai_score_may_affect_others_opts", []),
    )
    knowing_score_rule_affected_decision = models.IntegerField(
        label=getattr(Lexicon, "q_knowing_score_rule_affected_decision", ""),
        choices=getattr(Lexicon, "q_knowing_score_rule_affected_decision_opts", []),
    )

    # --- 追加: 戦略（複数選択 → Booleanで実装） ---

    strategy_max_self_payoff = models.BooleanField(blank=True, initial=False)
    strategy_fairness = models.BooleanField(blank=True, initial=False)
    strategy_avoid_conflict = models.BooleanField(blank=True, initial=False)
    strategy_probe = models.BooleanField(blank=True, initial=False)
    strategy_punish_unfair = models.BooleanField(blank=True, initial=False)
    strategy_other_text = models.LongStringField(blank=True,label = 'その他 (上記以外の戦略があればご記入ください)')

    # --- 追加: 参照点（単一選択） ---
    reference_point = models.IntegerField(
        label=getattr(Lexicon, "q_reference_point", "意思決定の際、最も重視した基準はどれですか？（1つ選択）"),
        choices=getattr(
            Lexicon,
            "q_reference_point_opts",
            [
                [1, "自分の利益"],
                [2, "相手の利益"],
                [3, "合計（効率性）"],
                [4, "利益の差（不平等）"],
                [5, "ルールそのもの"],
            ],
        ),
    )

    # --- 追加: 感情（1–7） ---
    emotion_anger = models.IntegerField(
        label=getattr(Lexicon, "q_emotion_anger", "怒り（1–7）"),
        choices=getattr(Lexicon, "q_emotion_anger_opts", []),
    )

    emotion_disappointment = models.IntegerField(
        label=getattr(Lexicon, "q_emotion_disappointment", "失望（1–7）"),
        choices=getattr(Lexicon, "q_emotion_disappointment_opts", []),
    )
    emotion_respected = models.IntegerField(
        label=getattr(Lexicon, "q_emotion_respected", "尊重されている（1–7）"),
        choices=getattr(Lexicon, "q_emotion_respected_opts", []),
    )

    emotion_trust = models.IntegerField(
        label=getattr(Lexicon, "q_emotion_trust", "信頼（1–7）"),
        choices=getattr(Lexicon, "q_emotion_trust_opts", []),
    )

    emotion_confusion = models.IntegerField(
        label=getattr(Lexicon, "q_emotion_confusion", "困惑（1–7）"),
        choices=getattr(Lexicon, "q_emotion_confusion_opts", []),
    )


    if Treatment == 2 or Treatment == 3:
        # --- 追加: AI態度（T2/T3想定） ---
        ai_tool_vs_agent = models.IntegerField(
            label=getattr(Lexicon, "q_ai_tool_vs_agent"),
            choices=getattr(Lexicon, "q_ai_tool_vs_agent_opts", [])
            )
        ai_deserves_fairness = models.IntegerField(
            label=getattr(Lexicon, "q_ai_deserves_fairness"),
            choices=getattr(Lexicon, "q_ai_deserves_fairness_opts", [])
        )
        ai_fairness_unimportant_if_no_money = models.IntegerField(
            label=getattr(Lexicon, "q_ai_fairness_unimportant_if_no_money"),
            choices=getattr(Lexicon, "q_ai_fairness_unimportant_if_no_money_opts", [])
        )
        ai_has_intentions = models.IntegerField(
            label=getattr(Lexicon, "q_ai_has_intentions"),
            choices=getattr(Lexicon, "q_ai_has_intentions_opts", [])
        )
        ai_has_strategy = models.IntegerField(
            label=getattr(Lexicon, "q_ai_has_strategy"),
            choices=getattr(Lexicon, "q_ai_has_strategy_opts", [])
        )
        ai_has_emotions = models.IntegerField(
            label=getattr(Lexicon, "q_ai_has_emotions"),
            choices=getattr(Lexicon, "q_ai_has_emotions_opts", [])
        )


# PAGES
class Start(Page):
    pass

def custom_export(players):
    yield [
        'label', 'id_in_group',
        'age', 'gender', 'affiliate',
        'consider_counterparty_payoff',
        'anger_unfair_offer',
        'chatgpt_use',
        'chatgpt_frequency',
        'knowing_ai_affected_decision',
        'consider_ai_payoff',
        'anger_unfair_ai_offer',
        'felt_humanness_or_trust',
        'knew_ai_score_may_affect_others',
        'knowing_score_rule_affected_decision',
        'strategy_max_self_payoff',
        'strategy_fairness',
        'strategy_avoid_conflict',
        'strategy_probe',
        'strategy_punish_unfair',
        'strategy_other_text',
        'reference_point',
        'emotion_anger',
        'emotion_disappointment',
        'emotion_respected',
        'emotion_trust',
        'emotion_confusion',
        'ai_tool_vs_agent',
        'ai_deserves_fairness',
        'ai_fairness_unimportant_if_no_money',
        'ai_has_intentions',
        'ai_has_strategy',
        'ai_has_emotions',
    ]
    for p in players:
        yield [
            p.participant.label, p.id_in_group,
            p.age, p.gender, p.affiliate,
            p.consider_counterparty_payoff,
            p.anger_unfair_offer,
            p.chatgpt_use,
            p.chatgpt_frequency,
            p.knowing_ai_affected_decision,
            p.consider_ai_payoff,
            p.anger_unfair_ai_offer,
            p.felt_humanness_or_trust,
            p.knew_ai_score_may_affect_others,
            p.knowing_score_rule_affected_decision,
            p.strategy_max_self_payoff,
            p.strategy_fairness,
            p.strategy_avoid_conflict,
            p.strategy_probe,
            p.strategy_punish_unfair,
            p.strategy_other_text,
            p.reference_point,
            p.emotion_anger,
            p.emotion_disappointment,
            p.emotion_respected,
            p.emotion_trust,
            p.emotion_confusion,
            p.ai_tool_vs_agent,
            p.ai_deserves_fairness,
            p.ai_fairness_unimportant_if_no_money,
            p.ai_has_intentions,
            p.ai_has_strategy,
            p.ai_has_emotions,
        ]

class Question1(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        base = ['age', 'gender', 'affiliate']

        if Treatment == 1:
            return base + [
                'consider_counterparty_payoff',
                'anger_unfair_offer',
                'chatgpt_use',
                'chatgpt_frequency',
            ]

        if Treatment == 2:
            return base + [
                'chatgpt_use',
                'chatgpt_frequency',
                'knowing_ai_affected_decision',
                'consider_ai_payoff',
                'anger_unfair_ai_offer',
                'felt_humanness_or_trust',
            ]

        return base + [
            'chatgpt_use',
            'chatgpt_frequency',
            'knowing_ai_affected_decision',
            'consider_ai_payoff',
            'anger_unfair_ai_offer',
            'felt_humanness_or_trust',
            'knew_ai_score_may_affect_others',
            'knowing_score_rule_affected_decision',
        ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(Lexicon=Lexicon)

class QuestionAI(Page):
    form_model = 'player'
    form_fields = ['ai_tool_vs_agent','ai_deserves_fairness','ai_fairness_unimportant_if_no_money','ai_has_intentions','ai_has_strategy','ai_has_emotions']

    @staticmethod
    def is_displayed(player):
        return Treatment != 1

class QuestionEmotion(Page):
    form_model = 'player'
    form_fields = ['emotion_anger','emotion_disappointment','emotion_respected','emotion_trust','emotion_confusion']

class Question2(Page):
    form_model = 'player'
    form_fields = ['strategy_max_self_payoff','strategy_fairness','strategy_avoid_conflict','strategy_probe','strategy_punish_unfair','strategy_other_text']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
        )


page_sequence = [Start, Question1, QuestionEmotion,QuestionAI, Question2]