"""Initial intro with rules and quiz"""
from otree.api import *

# Constants

class C(BaseConstants):
    """Constants for the intro_quiz app"""

    @staticmethod
    def add_indices(l):
        for i, item in enumerate(l):
            item['idx'] = i
        return l

    NAME_IN_URL = "intro_quiz"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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
    question1 = models.BooleanField(label="This study consists of 10 periods.")
    question2 = models.BooleanField(label="Each period consists of a hiring phase and a work phase.")
    question3 = models.BooleanField(label="In the hiring phase of each period, each employer <strong>must</strong> "
                                          "make a contract offer to one worker.")
    question4 = models.BooleanField(label="In the hiring phase of each period, workers review the offers they received "
                                          "and <strong>must</strong> accept one offer.")
    question5 = models.BooleanField(label="If a worker rejects an offer received from an employer in the hiring phase "
                                          "of a period, the worker <strong>will</strong> be able to receive another "
                                          "offer <strong>from the same employer in that period</strong>.")
    question6 = models.BooleanField(label="Employer offers include a salary and whether training is provided during "
                                          "the period. Regardless of the worker's effort decision during the "
                                          "subsequent work phase, the salary and training specified in the accepted "
                                          "offer must be provided.")
    question7 = models.BooleanField(label="Employers and workers who do not contract in the hiring phase of a period "
                                          "receive only their initial endowment for that period and do not complete "
                                          "the work phase. Employers do not receive revenue from worker effort and "
                                          "workers do not receive a salary from an employer.")
    question8 = models.BooleanField(label="In the work phase of each period, every hired worker must decide how much "
                                          "effort to exert. Higher levels of effort are <strong>more costly</strong> "
                                          "to the worker than lower levels of effort.")
    question9 = models.BooleanField(label="For every worker skill level, the higher the level of effort a worker "
                                          "chooses, the higher an employer's revenue is.")
    question10 = models.BooleanField(label="Worker's productivity is based on his/her skill level. The higher the "
                                           "worker's skill level, the higher the worker's productivity is and, thus, "
                                           "the higher the revenue for the employer is for a given effort level.")
    question11 = models.BooleanField(label="In the hiring phase in <strong>each</strong> of the 10 periods, every "
                                           "employer can again select <strong>any</strong> potential worker to make a "
                                           "contract offer to and every worker can freely accept one of the contract "
                                           "offers they receive.")

def prepare_error_message(correct_answer):
    return f"Your response is incorrect. {correct_answer} Please try again."


# Error messages for questions

def question1_error_message(player, value):
    if not value:
        return prepare_error_message("This study consists of 10 periods.")
    else:
        return None

def question2_error_message(player, value):
    if not value:
        return prepare_error_message("Each period consists of a hiring phase and a work phase.")
    else:
        return None

def question3_error_message(player, value):
    if value:
        return prepare_error_message("Each employer does not have to make a contract offer to a worker.")
    else:
        return None

def question4_error_message(player, value):
    if value:
        return prepare_error_message("Workers do not have to accept an offer.")
    else:
        return None

def question5_error_message(player, value):
    if value:
        return prepare_error_message("If a worker rejects an offer received from an employer in the hiring phase of a "
                                     "period, the worker will not be able to receive another offer from the same "
                                     "employer in that period. ")
    else:
        return None

def question6_error_message(player, value):
    if not value:
        return prepare_error_message("Employer offers include a salary and whether training is provided during the "
                                     "period. The specified salary and training must be provided.")
    else:
        return None

def question7_error_message(player, value):
    if not value:
        return prepare_error_message("Employers and workers who do not contract do not receive revenue from worker "
                                     "effort or a salary respectively.")
    else:
        return None

def question8_error_message(player, value):
    if not value:
        return prepare_error_message("Every hired worker must decide how much effort to exert. Higher levels of "
                                     "effort are more costly to them.")
    else:
        return None

def question9_error_message(player, value):
    if not value:
        return prepare_error_message("The higher the level of effort a worker chooses, the higher an employer's "
                                     "revenue is.")
    else:
        return None

def question10_error_message(player, value):
    if not value:
        return prepare_error_message("Worker's productivity is based on his/her skill level. The higher the "
                                     "worker's skill level, the higher the worker's productivity is and, thus, "
                                     "the higher the revenue for the employer is for a given effort level.")
    else:
        return None

def question11_error_message(player, value):
    if not value:
        return prepare_error_message("In the hiring phase in each of the 10 periods, every employer can again "
                                     "select any potential worker to make a contract offer to and every worker can "
                                     "freely accept one of the contract offers they receive.")
    else:
        return None

# Pages

class Consent(Page):
    """Intro page with consent"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict(
            participation_fee = cu(session.config["participation_fee"]).to_real_world_currency(session)
        )


class Instructions1(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
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
    form_fields = ['question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7',
                   'question8', 'question9', 'question10', 'question11']


page_sequence = [Consent, Instructions1, Instructions2, Instructions3, Quiz1]
