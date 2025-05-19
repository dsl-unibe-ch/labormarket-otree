"""Initial intro with rules and quiz"""
from otree.api import *

# Constants

class C(BaseConstants):
    """Constants for the intro_quiz app"""
    NAME_IN_URL = "intro_quiz"
    PLAYERS_PER_GROUP = None
    TRUE = 'True'
    FALSE = 'False'
    TRUE_FALSE = [TRUE, FALSE]
    QUESTIONS = [
        dict(text="This study consists of 10 periods.", choices=[TRUE_FALSE], correct=TRUE),
        dict(text="Each period consists of a hiring phase and a work phase.", choices=[TRUE_FALSE], correct=TRUE),
        dict(text="In the hiring phase of each period, each employer <strong>must</strong> make a contract offer to "
                  "one worker.", choices=[TRUE_FALSE], correct=FALSE),
        dict(text="In the hiring phase of each period, workers review the offers they received and "
                  "<strong>must</strong> accept one offer.", choices=[TRUE_FALSE], correct=FALSE),
        dict(text="If a worker rejects an offer received from an employer in the hiring phase of a period, the worker "
                  "<strong>will</strong> be able to receive another offer <strong>from the same employer in that "
                  "period</strong>.", choices=[TRUE_FALSE], correct=FALSE),
        dict(text="Employer offers include a salary and whether training is provided during the period. Regardless "
                  "of the worker's effort decision during the subsequent work phase, the salary and training "
                  "specified in the accepted offer must be provided.", choices=[TRUE_FALSE], correct=TRUE),
        dict(text="Employers and workers who do not contract in the hiring phase of a period receive only their "
                  "initial endowment for that period and do not complete the work phase. Employers do not receive "
                  "revenue from worker effort and workers do not receive a salary from an employer.",
             choices=[TRUE_FALSE], correct=TRUE),
        dict(text="In the work phase of each period, every hired worker must decide how much effort to exert. Higher "
                  "levels of effort are <strong>more costly</strong> to the worker than lower levels of effort.",
             choices=[TRUE_FALSE], correct=TRUE),
        dict(text="For every worker skill level, the higher the level of effort a worker chooses, the higher an "
                  "employer's revenue is.", choices=[TRUE_FALSE], correct=TRUE),
        dict(text="Worker's productivity is based on his/her skill level. The higher the worker's skill level, the "
                  "higher the worker's productivity is and, thus, the higher the revenue for the employer is for "
                  "a given effort level.", choices=[TRUE_FALSE], correct=TRUE),
        dict(text="In the hiring phase in <strong>each</strong> of the 10 periods, every employer can again select "
                  "<strong>any</strong> potential worker to make a contract offer to and every worker can freely "
                  "accept one of the contract offers they receive.", choices=[TRUE_FALSE], correct=TRUE),
    ]
    NUM_ROUNDS = len(QUESTIONS)

# Objects

def multiplier_to_table_item(mult_tuple: tuple[int, int]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [round(effort * multiplier) for effort in range(1, 11)]
    }

class Subsession(BaseSubsession):
    """Subsession object for quiz"""

    @property
    def skill_table(self):
        """Prepare skill table for template"""
        return list(map(
            multiplier_to_table_item,
            enumerate(self.session.config["skill_multipliers"])
        ))

    @property
    def effort_table(self):
        return self.session.config["effort_costs"]

class Group(BaseGroup):
    """Group object for quiz"""

class Player(BasePlayer):
    """Player object for quiz"""
    response = models.StringField()
    is_correct = models.BooleanField()

# Pages

class Consent(Page):
    """Intro page with consent"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing participation fee"""
        session = player.session

        return dict(
            participation_fee = cu(session.config["participation_fee"]).to_real_world_currency(session)
        )


class Instructions1(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing participation fee"""
        session = player.session

        return dict(
            participation_fee=cu(session.config["participation_fee"]).to_real_world_currency(session)
        )

class Instructions2(Page):
    """Intro page with instructions"""

class Instructions3(Page):
    """Intro page with instructions"""


class Quiz1(Page):
    """Quiz page to test comprehension"""
    form_model = 'player'
    form_fields = ['response']

    @staticmethod
    def vars_for_template(player):
        q = C.QUESTIONS[player.round_number - 1]
        return dict(question=q['text'], choices=q['choices'])

    # @staticmethod
    # def app_after_this_page(player, upcoming_apps):
    #     if player.whatever:
    #         return "public_goods"
    #
    # @staticmethod
    # def error_message(player, values):
    #     """Runs before oTree decides whether to show the page again."""
    #     r = player.round_number
    #
    #     correct = C.QUESTIONS[r - 1]['correct']
    #     if values['response'] != correct:
    #         return f"Your response is incorrect. Please try again."
    #     # returning None lets the player continue

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     q = C.QUESTIONS[player.round_number - 1]
    #     player.is_correct = (player.response == q['correct'])
    #     if not player.is_correct:
    #         # Don't proceed to the next page.

page_sequence = [Consent, Instructions1, Instructions2, Instructions3, Quiz1]
