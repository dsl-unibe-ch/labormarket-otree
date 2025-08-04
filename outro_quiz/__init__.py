"""Initial outro with rules and quiz"""
from typing import Iterator, List

from otree.api import *
from otree.currency import RealWorldCurrency

from outro_quiz.quiz import *

# Constants

class C(BaseConstants):
    """Constants for the outro_quiz app"""

    @staticmethod
    def add_indices(l):
        for i, item in enumerate(l):
            item['idx'] = i
        return l

    NUM_ROUNDS = 1
    NAME_IN_URL = "outro_quiz"
    PLAYERS_PER_GROUP = None

    MANAGER1_ROLE = "Manager"
    MANAGER2_ROLE = "Manager"
    MANAGER3_ROLE = "Manager"
    EMPLOYEE1_ROLE = "Employee"
    EMPLOYEE2_ROLE = "Employee"
    EMPLOYEE3_ROLE = "Employee"

# Functions

def multiplier_to_table_item(mult_tuple: tuple[int, int]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [effort * multiplier for effort in range(1, 11)]
    }

def custom_export(players) -> Iterator[List[str | int | float]]:
    yield [
        "participant_code",
        "peq1",
        "peq2",
        "peq3",
        "peq4",
        "peq5",
        "peq6",
        "peq7",
        "peq8",
        "peq9",
        "peq10",
        "peq11",
        "peq12",
        "peq13",
        "peq14",
        "peq15",
        "peq16",
        "peq17",
        "gender",
        "age",
        "grade_status",
        "major",
        "gpa",
        "econ_classes",
        "risk_comfort",
        "strategy_notes",
    ]

    latest_session_id = max(p.session.id for p in players)

    for player in players:
        if player.session.id == latest_session_id:
            yield [
                player.participant.code,
                player.peq_quiz1,
                player.peq_quiz2,
                player.peq_quiz3,
                player.peq_quiz4,
                player.peq_quiz5,
                player.peq_quiz6,
                player.peq_quiz7,
                player.peq_quiz8,
                player.peq_quiz9,
                player.peq_quiz10,
                player.peq_quiz11,
                player.peq_quiz12,
                player.peq_quiz13,
                player.peq_quiz14,
                player.peq_quiz15,
                player.peq_quiz16,
                player.peq_quiz17,
                player.demographic_quiz1,
                player.demographic_quiz2,
                player.demographic_quiz3,
                player.demographic_quiz4,
                player.demographic_quiz5,
                player.demographic_quiz6,
                player.demographic_quiz7,
                player.demographic_quiz8,
            ]

# Objects

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


class Player(BasePlayer):
    """Player object for quiz"""

    peq_quiz1 = models.StringField()
    peq_quiz2 = models.StringField()
    peq_quiz3 = models.StringField()
    peq_quiz4 = models.StringField()
    peq_quiz5 = models.StringField()
    peq_quiz6 = models.StringField()
    peq_quiz7 = models.StringField()
    peq_quiz8 = models.StringField()
    peq_quiz9 = models.StringField()
    peq_quiz10 = models.StringField()
    peq_quiz11 = models.StringField()
    peq_quiz12 = models.StringField()
    peq_quiz13 = models.StringField()
    peq_quiz14 = models.StringField()
    peq_quiz15 = models.StringField()
    peq_quiz16 = models.StringField()
    peq_quiz17 = models.StringField()

    demographic_quiz1 = models.StringField()
    demographic_quiz2 = models.IntegerField()
    demographic_quiz3 = models.StringField()
    demographic_quiz4 = models.StringField()
    demographic_quiz5 = models.StringField()
    demographic_quiz6 = models.IntegerField()
    demographic_quiz7 = models.IntegerField()
    demographic_quiz8 = models.LongStringField()

    @property
    def printable_role(self):
        role_to_string = {"Manager": "Employer", "Employee": "Worker"}
        return role_to_string[self.role]

    skill = models.IntegerField(initial=1)

    response = models.IntegerField()
    is_correct = models.BooleanField()


class Group(BaseGroup):
    """Group object for quiz"""

    @property
    def managers(self):
        """Return all Manager players from the current group"""
        return [player for player in self.get_players() if player.role == "Manager"]

    @property
    def employees(self):
        """Return all Employee players from the current group"""
        return [player for player in self.get_players() if player.role == "Employee"]


# Pages

class PEQ(Page):
    """Post-experiment questionnaire"""
    form_model = "player"
    form_fields = [f"peq_quiz{i}" for i in range(1, 18)]

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(player))


class DemographicQuiz(Page):
    form_model = "player"
    form_fields = [f"demographic_quiz{i}" for i in range(1, 9)]

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(player))


class Conclusion(Page):

    @staticmethod
    def vars_for_template(player: "Player"):
        session = player.session
        participation_fee = RealWorldCurrency(session.config["participation_fee"])
        real_world_currency_per_point = session.config["real_world_currency_per_point"]

        # Here we have to prevent theoretically possible negative values, otherwise the participants will owe money.
        real_payoff = max(player.participant.payoff, cu(0)).to_real_world_currency(session)
        total_payment = real_payoff + participation_fee

        return dict(real_world_currency_per_point=real_world_currency_per_point, participation_fee=participation_fee,
                    real_payoff=real_payoff, total_payment=total_payment)


page_sequence = [PEQ, DemographicQuiz, Conclusion]