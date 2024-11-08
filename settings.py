"""Settings file for labormarket oTree experiment"""
from os import environ

SESSION_CONFIGS = [
    dict(
        name="labor_market",
        app_sequence=["labor_market"],
        num_demo_participants=10,
        max_rounds=10
    ),
    dict(
        name="labor_market_with_quiz",
        app_sequence=["intro_quiz", "labor_market"],
        num_demo_participants=10,
        max_rounds=10
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    skill_multipliers=[1.00, 1.40, 1.77, 2.11, 2.42, 2.70, 2.95, 3.17, 3.36, 3.52, 3.65, 3.75, 3.82, 3.86, 3.87],
    doc="",
    randomize_roles=False
)

SESSION_FIELDS = ["skill_table"]
PARTICIPANT_FIELDS = ["dropout"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7341359800173'
