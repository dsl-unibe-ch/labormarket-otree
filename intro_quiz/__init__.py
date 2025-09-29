"""Initial intro with rules and quiz"""
import random
from typing import List

from otree.api import *
from otree.currency import RealWorldCurrency

from intro_quiz.quiz import *

# Constants

class C(BaseConstants):
    """Constants for the intro_quiz app"""

    @staticmethod
    def add_indices(l):
        for i, item in enumerate(l):
            item['idx'] = i
        return l

    NUM_ROUNDS = 1
    NAME_IN_URL = "intro_quiz"
    PLAYERS_PER_GROUP = None

    MANAGER1_ROLE = "Manager"
    MANAGER2_ROLE = "Manager"
    MANAGER3_ROLE = "Manager"
    EMPLOYEE1_ROLE = "Employee"
    EMPLOYEE2_ROLE = "Employee"
    EMPLOYEE3_ROLE = "Employee"

def multiplier_to_table_item(mult_tuple: tuple[int, int]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [effort * multiplier for effort in range(1, 11)]
    }

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

@staticmethod
def creating_session(subsession: Subsession):
    """Set per-session participant data"""

    # If session config dictates, reshuffle participants randomly
    if subsession.session.config["randomize_roles"]:
        subsession.group_randomly()
    for group in subsession.get_groups():
        # Set initial skills according to session config
        for index, player in enumerate(group.employees):
            player.skill = subsession.session.config["starting_skills"][index]

    group_matrix = subsession.get_group_matrix()
    print(f"Group matrix: {group_matrix}")
    subsession.session.vars["frozen_matrix"] = group_matrix


class Player(BasePlayer):
    """Player object for quiz"""

    # Visible "name" for the player (company name or employee nickname)
    label = models.StringField()

    # Skill level
    skill = models.IntegerField(initial=1)

    @property
    def q_2_7_text(self):
        session = self.session
        market = session.config["market"]

        return dict(
            homoogenous_low="In the first period, all workers start with a skill level of 1.",
            homoogenous_high="In the first period, all workers start with a skill level of 5.",
            heterogenous="In the first period, three workers start with a skill level of 1 "
                         "and three workers start with a skill level of 5."
        )[market]

    response = models.IntegerField()
    is_correct = models.BooleanField()


class Group(BaseGroup):
    """Group object for quiz"""

    @property
    def managers(self) -> List[Player]:
        """Return all Manager players from the current group"""
        return [player for player in self.get_players() if player.role == "Manager"]

    @property
    def employees(self) -> List[Player]:
        """Return all Employee players from the current group"""
        return [player for player in self.get_players() if player.role == "Employee"]


def prepare_error_message(correct_answer):
    return f"Your response is incorrect. {correct_answer} Please try again."

# Pages

class Consent(Page):
    """Intro page with consent"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict(
            participation_fee = RealWorldCurrency(session.config["participation_fee"])
        )


class Instructions1(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict(
            participation_fee=RealWorldCurrency(session.config["participation_fee"])
        )


class Instructions2(Page):
    """Intro page with instructions"""
    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict (
            max_wage=session.config["max_wage"]
        )

class Instructions3(Page):
    """Intro page with instructions"""


class Instructions4(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session
        skill_multipliers = session.config["skill_multipliers"]

        return dict(
            example=f"For example, increasing a worker's skill level from 1 to 2 "
                    f"boosts productivity from {skill_multipliers[0]} to {skill_multipliers[1]} "
                    f"(an increase of {skill_multipliers[1] - skill_multipliers[0]}), "
                    f"while increasing the skill level from 5 to 6 "
                    f"only raises productivity from {skill_multipliers[4]} to {skill_multipliers[5]} "
                    f"(an increase of {skill_multipliers[5] - skill_multipliers[4]})."
        )


class Instructions5(Page):
    """Intro page with instructions"""

    MARKET_DESCRIPTION = dict(
        homoogenous_low="all workers start with a skill level of 1",
        homoogenous_high="all workers start with a skill level of 5",
        heterogenous="three workers start with a skill level of 1 and three workers start with a skill level of 5"
    )

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session
        market = session.config["market"]
        skill_multipliers = session.config["skill_multipliers"]

        market_productivity = dict(
            homoogenous_low=f"all workers have a productivity of {skill_multipliers[0]}",
            homoogenous_high=f"all workers have a productivity of {skill_multipliers[4]}",
            heterogenous=f"three workers have a productivity of {skill_multipliers[0]} "
                         f"and three workers have a productivity of {skill_multipliers[4]}"
        )

        return dict(
            market_description=Instructions5.MARKET_DESCRIPTION[market],
            market_productivity=market_productivity[market],
            group_id=player.group_id,
            worker_info=f"Your skill level in the first period is {player.skill}."
                    if player.role == "Employee" else None
        )


class Instructions6(Page):
    """Intro page with instructions"""

class Instructions7(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player):
        """Providing variables for template"""
        return dict(employee_endowment=player.session.config["employee_endowment"])

class Instructions8(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player):
        """Providing variables for template"""
        session = player.session

        return dict(
            manager_endowment=session.config["manager_endowment"],
            participation_fee = RealWorldCurrency(session.config["participation_fee"])
        )

class Instructions9(Page):
    """Intro page with instructions"""

class Instructions10(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player):
        """Providing variables for template"""
        session = player.session

        return dict(
            employee_endowment=session.config["employee_endowment"],
            manager_endowment=session.config["manager_endowment"],
            training_cost=session.config["training_cost"],
        )

class Quiz1(Page):
    """Quiz page to test comprehension"""

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(0, player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(0, player), answers=get_answers(0), hints=get_hints(0, player))


class Quiz2(Page):
    """Quiz page to test comprehension"""

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(1, player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(1, player), answers=get_answers(1), hints=get_hints(1, player))

class Quiz3(Page):
    """Quiz page to test comprehension"""

    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(2, player))

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions=get_questions(2, player), answers=get_answers(2), hints=get_hints(2, player))


# pages.py
class Question(Page):
    form_model  = "player"
    form_fields = ["response"]

    @staticmethod
    def vars_for_template(player):
        q = C.QUIZ_1_QUESTIONS[player.round_number - 1]
        return dict(question=q["text"], choices=q["choices"])

    @staticmethod
    def before_next_page(player, timeout_happened):
        """Mark right/wrong, but ALWAYS continue to Feedback."""
        idx = player.participant.q_idx
        q = C.QUIZ_1_QUESTIONS[idx]["correct"]
        player.is_correct = (player.response == q)


class Feedback(Page):
    @staticmethod
    def vars_for_template(player):
        idx = player.participant.q_idx
        q   = C.QUIZ_1_QUESTIONS[idx]
        text = q["text"]
        return dict(
            question=text,
            correct_answer=q["correct"],
            correct_text=q.get("correct_text", text),
            your_answer=player.response,
            right=player.is_correct,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        """Advance pointer only if answer was correct."""
        if player.is_correct:
            player.participant.q_idx += 1

    @staticmethod
    def is_displayed(player):
        """Hide Feedback once we ran out of questions."""
        return player.participant.q_idx < len(C.QUIZ_1_QUESTIONS)

page_sequence = [
    Consent,
    Instructions1, Instructions2, Instructions3,
    Quiz1,
    Instructions4, Instructions5, Instructions6,
    Quiz2,
    Instructions7, Instructions8, Instructions9, Instructions10,
    Quiz3
]
