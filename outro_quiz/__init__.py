"""Initial outro with rules and quiz"""
from otree.api import *
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

# Objects

def multiplier_to_table_item(mult_tuple: tuple[int, int]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [effort * multiplier for effort in range(1, 11)]
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


class Player(BasePlayer):
    """Player object for quiz"""

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
    """Quiz page to test comprehension"""

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(player))

class DemographicQuiz(Page):
    """Quiz page to test comprehension"""

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(player))

page_sequence = [DemographicQuiz]