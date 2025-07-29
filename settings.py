"""Settings file for labormarket oTree experiment"""
from os import environ

SESSION_CONFIGS = [
    dict(
        name="labor_market",
        app_sequence=["labor_market"],
        num_demo_participants=6,
        max_rounds=10
    ),
    dict(
        name="labor_market_with_quizzes",
        app_sequence=["intro_quiz", "labor_market", "outro_quiz"],
        num_demo_participants=6,
        max_rounds=10
    ),
    dict(
        name="outro_quiz",
        app_sequence=["outro_quiz"],
        num_demo_participants=6,
        max_rounds=10
    ),
]


# Starting skills based on the market
STARTING_SKILLS_BY_MARKET = dict(
    homoogenous_low=[1, 1, 1],
    homoogenous_high=[5, 5, 5],
    heterogenous=[5, 5, 1]
)

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    market="heterogenous",
    skill_multipliers=[100, 140, 177, 211, 242, 270, 295, 317, 336, 352, 365, 375, 382, 386, 387],
    effort_costs=[0, 20, 40, 60, 100, 140, 180, 240, 300, 360],
    employee_endowment=400,
    manager_endowment=800,
    base_revenue=1,
    training_productivity_multiplier=0.5,
    training_cost=50,
    max_wage=3000,
    doc="",
    randomize_roles=False
)

# Setting the starting_skills value depending on the market.
SESSION_CONFIG_DEFAULTS.update(starting_skills=STARTING_SKILLS_BY_MARKET[SESSION_CONFIG_DEFAULTS["market"]])

SESSION_FIELDS = ["skill_table"]
PARTICIPANT_FIELDS = ["dropout", "q_idx"]

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
