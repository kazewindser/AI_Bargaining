from os import environ

SESSION_CONFIGS = [
    dict(
        name='Test',
        display_name='Test',
        app_sequence=['AI','BreakForPayoff','Payoff'],
        num_demo_participants=4,
    ),
    dict(
        name='HumanT1',
        display_name='HumanT1',
        app_sequence=['Instruction', 'Quiz', 'preSurvey', 'Human', 'BreakForPayoff','Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
    dict(
        name='AIT2',
        display_name='AIT2',
        app_sequence=['Instruction', 'Quiz', 'preSurvey', 'AI','BreakForPayoff', 'Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
    dict(
        name='AIT3',
        display_name='AIT3',
        app_sequence=['Instruction', 'Quiz', 'preSurvey', 'AI','BreakForPayoff', 'Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
]

Treatment = 3  # 1: Human, 2: AI_NObeneficial 3: AI_Beneficial

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=500, doc=""
)

PARTICIPANT_FIELDS = ['PairedLabel','Discounted_points_Per_Round','ROLE',
                      'SelectedRound','Final_Point_Payoff',
                      'T3_AI_P1_Discounted_points','T3_AI_P2_Discounted_points',
                      'T3_whether_getAI_OFFER','id_sameAIpoints']
SESSION_FIELDS = []


# rooms
ROOMS = [
    dict(
        name='pclab',
        display_name='社研PCラボ',
        participant_label_file='_rooms/pclab.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
    dict(
        name='virtual_Lab',
        display_name='Room for virtual Lab 40 subjects (sub**)',
        participant_label_file='_rooms/virtualLab.txt',
    )
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1493461249988'
