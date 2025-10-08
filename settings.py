"""Settings file for labor market oTree experiment"""
from os import environ

# Starting skills based on the market
STARTING_SKILLS_BY_MARKET = dict(
    homogeneous_low=[1, 1, 1, 1, 1, 1],
    homogeneous_high=[5, 5, 5, 5, 5, 5],
    heterogeneous=[5, 5, 5, 1, 1, 1]
)

SESSION_CONFIGS = [
    dict(
        name="experiment_heterogeneous",
        app_sequence=["intro_quiz", "labor_market", "outro_quiz"],
        num_demo_participants=12,
        max_rounds=10,
        market="heterogeneous",
        starting_skills=STARTING_SKILLS_BY_MARKET["heterogeneous"]
    ),
    dict(
        name="experiment_homogeneous_low",
        app_sequence=["intro_quiz", "labor_market", "outro_quiz"],
        num_demo_participants=12,
        max_rounds=10,
        market="homogeneous_low",
        starting_skills=STARTING_SKILLS_BY_MARKET["homogeneous_low"]
    ),
    dict(
        name="experiment_homogeneous_high",
        app_sequence=["intro_quiz", "labor_market", "outro_quiz"],
        num_demo_participants=12,
        max_rounds=10,
        market="homogeneous_high",
        starting_skills=STARTING_SKILLS_BY_MARKET["homogeneous_high"]
    ),
    dict(
        name="test_all",
        app_sequence=["intro_quiz", "labor_market", "outro_quiz"],
        num_demo_participants=12,
        max_rounds=3,
        market="heterogeneous",
        starting_skills=STARTING_SKILLS_BY_MARKET["heterogeneous"]
    ),
    dict(
        name="test_simulation",
        app_sequence=["labor_market", "outro_quiz"],
        num_demo_participants=12,
        max_rounds=3,
        market="heterogeneous",
        starting_skills=STARTING_SKILLS_BY_MARKET["heterogeneous"]
    ),
    dict(
        name="test_outro",
        app_sequence=["outro_quiz"],
        num_demo_participants=12,
        max_rounds=3,
        market="heterogeneous",
        starting_skills=STARTING_SKILLS_BY_MARKET["heterogeneous"]
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.0025,
    participation_fee=5.00,
    market="heterogeneous",
    skill_multipliers=[100, 140, 177, 211, 242, 270, 295, 317, 336, 352, 365, 375, 382, 386, 387],
    effort_costs=[0, 20, 40, 60, 100, 140, 180, 240, 300, 360],
    employee_endowment=400,
    manager_endowment=800,
    base_revenue=1,
    training_productivity_multiplier=0.5,
    training_cost=50,
    max_wage=1500,
    doc="""
        Edit the 'market' parameter to specify what initial skill the workers will have.
        The possible values and their corresponding skill levels are the following.<br/> 
        homogeneous_low: [1, 1, 1, 1, 1, 1]<br/>
        homogeneous_high: [5, 5, 5, 5, 5, 5]<br/>
        heterogeneous: [5, 5, 5, 1, 1, 1]
        """,
    randomize_roles=False
)

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

ROOMS = [
    dict(
        name="excenlab",
        display_name="excenlab.txt",
        participant_label_file="_rooms/excenlab.txt",
    ),
    dict(name="live_demo", display_name="Room for live demo (no participant labels)"),
]