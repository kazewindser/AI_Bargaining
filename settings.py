from os import environ

SESSION_CONFIGS = [
    dict(
        name='Test',
        display_name='Test',
        app_sequence=['Quiz'],
        num_demo_participants=1,
    ),
    dict(
        name='HumanT1',
        display_name='HumanT1',
        app_sequence=['Instruction', 'Quiz', 'Practise', 'Human', 'Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
    dict(
        name='AIT2',
        display_name='AIT2',
        app_sequence=['Instruction', 'Quiz', 'Practise', 'AI', 'Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
    dict(
        name='AIT3',
        display_name='AIT3',
        app_sequence=['Instruction', 'Quiz', 'Practise', 'AI', 'Questionnaire', 'Payoff'],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

Treatment = 1   # 1: Human, 2: AI_NObeneficial 3: AI_Beneficial

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1493461249988'
