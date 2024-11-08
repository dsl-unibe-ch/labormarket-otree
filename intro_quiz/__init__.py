"""Initial intro with rules and quiz"""
from otree.api import *

# Constants

class C(BaseConstants):
    """Constants for the intro_quiz app"""
    NAME_IN_URL = "intro_quiz"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

# Objects

def multiplier_to_table_item(mult_tuple: tuple[int, float]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [round(10 * effort * multiplier) for effort in range(1, 11)]
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

class Group(BaseGroup):
    """Group object for quiz"""

class Player(BasePlayer):
    """Player object for quiz"""

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


class Instructions(Page):
    """Intro page with instructions"""


class Quiz(Page):
    """Quiz page to test comprehension"""

page_sequence = [Consent, Instructions, Quiz]
