"""Initial intro with rules and quiz"""
import random
from typing import List

from otree.api import *
from otree.currency import RealWorldCurrency

from intro_quiz.quiz import *
from agent.config import should_use_agent

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
    MANAGER4_ROLE = "Manager"
    MANAGER5_ROLE = "Manager"
    MANAGER6_ROLE = "Manager"
    EMPLOYEE1_ROLE = "Employee"
    EMPLOYEE2_ROLE = "Employee"
    EMPLOYEE3_ROLE = "Employee"
    EMPLOYEE4_ROLE = "Employee"
    EMPLOYEE5_ROLE = "Employee"
    EMPLOYEE6_ROLE = "Employee"

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
            homogeneous_low="In the first period, all workers start with a skill level of 1.",
            homogeneous_high="In the first period, all workers start with a skill level of 5.",
            heterogeneous="In the first period, three workers start with a skill level of 1 "
                         "and three workers start with a skill level of 5."
        )[market]

    response = models.IntegerField()
    is_correct = models.BooleanField()

    # Quiz 1 responses (11 questions, True/False)
    q1_1 = models.IntegerField(blank=True)
    q1_2 = models.IntegerField(blank=True)
    q1_3 = models.IntegerField(blank=True)
    q1_4 = models.IntegerField(blank=True)
    q1_5 = models.IntegerField(blank=True)
    q1_6 = models.IntegerField(blank=True)
    q1_7 = models.IntegerField(blank=True)
    q1_8 = models.IntegerField(blank=True)
    q1_9 = models.IntegerField(blank=True)
    q1_10 = models.IntegerField(blank=True)
    q1_11 = models.IntegerField(blank=True)
    
    # Quiz 2 responses (8 questions max, True/False)
    q2_1 = models.IntegerField(blank=True)
    q2_2 = models.IntegerField(blank=True)
    q2_3 = models.IntegerField(blank=True)
    q2_4 = models.IntegerField(blank=True)
    q2_5 = models.IntegerField(blank=True)
    q2_6 = models.IntegerField(blank=True)
    q2_7 = models.IntegerField(blank=True)
    q2_8 = models.IntegerField(blank=True)
    
    # Quiz 3 responses (8 questions, multiple choice)
    q3_1 = models.IntegerField(blank=True)
    q3_2 = models.IntegerField(blank=True)
    q3_3 = models.IntegerField(blank=True)
    q3_4 = models.IntegerField(blank=True)
    q3_5 = models.IntegerField(blank=True)
    q3_6 = models.IntegerField(blank=True)
    q3_7 = models.IntegerField(blank=True)
    q3_8 = models.IntegerField(blank=True)
    
    # Track quiz completion (optional, useful for validation)
    quiz1_complete = models.BooleanField(initial=False)
    quiz2_complete = models.BooleanField(initial=False)
    quiz3_complete = models.BooleanField(initial=False)


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

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None


class Instructions1(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict(
            participation_fee=RealWorldCurrency(session.config["participation_fee"])
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None


class Instructions2(Page):
    """Intro page with instructions"""
    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict (
            max_wage=session.config["max_wage"]
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

class Instructions3(Page):
    """Intro page with instructions"""

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None


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

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None


class Instructions5(Page):
    """Intro page with instructions"""

    MARKET_DESCRIPTION = dict(
        homogeneous_low="all workers start with a skill level of 1",
        homogeneous_high="all workers start with a skill level of 5",
        heterogeneous="three workers start with a skill level of 1 and three workers start with a skill level of 5"
    )

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session
        market = session.config["market"]
        skill_multipliers = session.config["skill_multipliers"]

        market_productivity = dict(
            homogeneous_low=f"all workers have a productivity of {skill_multipliers[0]}",
            homogeneous_high=f"all workers have a productivity of {skill_multipliers[4]}",
            heterogeneous=f"three workers have a productivity of {skill_multipliers[0]} "
                         f"and three workers have a productivity of {skill_multipliers[4]}"
        )

        return dict(
            market_description=Instructions5.MARKET_DESCRIPTION[market],
            market_productivity=market_productivity[market],
            group_id=player.group_id,
            worker_info=f"Your skill level in the first period is <strong>{player.skill}</strong>."
                    if player.role == "Employee" else None
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None


class Instructions6(Page):
    """Intro page with instructions"""

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

class Instructions7(Page):
    """Intro page with instructions"""

    @staticmethod
    def vars_for_template(player):
        """Providing variables for template"""
        return dict(employee_endowment=player.session.config["employee_endowment"])

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

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

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

class Instructions9(Page):
    """Intro page with instructions"""

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

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

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

class Quiz1(Page):
    """Quiz page to test comprehension - supports both JS and form submission"""
    
    form_model = 'player'
    form_fields = ['q1_1', 'q1_2', 'q1_3', 'q1_4', 'q1_5', 'q1_6', 
                   'q1_7', 'q1_8', 'q1_9', 'q1_10', 'q1_11']
    
    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(0, player))
    
    @staticmethod
    def js_vars(player: "Player"):
        """For JavaScript-based quiz (human participants)"""
        return dict(
            questions=get_questions(0, player), 
            answers=get_answers(0), 
            hints=get_hints(0, player)
        )
    
    @staticmethod
    def error_message(player: Player, values):
        """Validate answers for bot/form submission"""
        correct_answers = get_answers(0)
        errors = {}
        
        # Only validate if at least one field is filled (indicates form submission)
        if any(values.get(f'q1_{i}') is not None for i in range(1, 12)):
            for i in range(11):
                field = f'q1_{i+1}'
                if values.get(field) != correct_answers[i]:
                    hints = get_hints(0, player)
                    errors[field] = hints[i][0]  # Show incorrect hint
        
        return errors if errors else None

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

    @staticmethod
    def get_timeout_submission(player: Player):
        if not should_use_agent(player):
            return {}
        answers = get_answers(0)
        return {f"q1_{i + 1}": answers[i] for i in range(len(answers))}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        """Mark quiz as complete"""
        player.quiz1_complete = True


class Quiz2(Page):
    """Quiz page to test comprehension - supports both JS and form submission"""
    
    @staticmethod
    def get_form_fields(player: Player):
        """Dynamic form fields based on role"""
        base_fields = ['q2_1', 'q2_2', 'q2_3', 'q2_4', 'q2_5', 'q2_6', 'q2_7']
        if player.role == "Employee":
            base_fields.append('q2_8')
        return base_fields
    
    form_model = 'player'
    
    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(1, player))
    
    @staticmethod
    def js_vars(player: "Player"):
        """For JavaScript-based quiz (human participants)"""
        return dict(
            questions=get_questions(1, player), 
            answers=get_answers(1), 
            hints=get_hints(1, player)
        )
    
    @staticmethod
    def error_message(player: Player, values):
        """Validate answers for bot/form submission"""
        correct_answers = get_answers(1)
        form_fields = Quiz2.get_form_fields(player)
        errors = {}
        
        # Only validate if at least one field is filled
        if any(values.get(field) is not None for field in form_fields):
            for i, field in enumerate(form_fields):
                if values.get(field) != correct_answers[i]:
                    hints = get_hints(1, player)
                    errors[field] = hints[i][0]
        
        return errors if errors else None

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

    @staticmethod
    def get_timeout_submission(player: Player):
        if not should_use_agent(player):
            return {}
        form_fields = Quiz2.get_form_fields(player)
        answers = get_answers(1)
        return {field: answers[i] for i, field in enumerate(form_fields)}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        """Mark quiz as complete"""
        player.quiz2_complete = True


class Quiz3(Page):
    """Quiz page to test comprehension - supports both JS and form submission"""
    
    form_model = 'player'
    form_fields = ['q3_1', 'q3_2', 'q3_3', 'q3_4', 'q3_5', 'q3_6', 'q3_7', 'q3_8']
    
    @staticmethod
    def vars_for_template(player: "Player"):
        return dict(questions=get_questions(2, player))
    
    @staticmethod
    def js_vars(player: "Player"):
        """For JavaScript-based quiz (human participants)"""
        return dict(
            questions=get_questions(2, player), 
            answers=get_answers(2), 
            hints=get_hints(2, player)
        )
    
    @staticmethod
    def error_message(player: Player, values):
        """Validate answers for bot/form submission"""
        correct_answers = get_answers(2)
        errors = {}
        
        # Only validate if at least one field is filled
        if any(values.get(f'q3_{i}') is not None for i in range(1, 9)):
            for i in range(8):
                field = f'q3_{i+1}'
                if values.get(field) != correct_answers[i]:
                    hints = get_hints(2, player)
                    errors[field] = hints[i][0]
        
        return errors if errors else None

    @staticmethod
    def get_timeout_seconds(player: Player):
        if should_use_agent(player):
            return 1
        return None

    @staticmethod
    def get_timeout_submission(player: Player):
        if not should_use_agent(player):
            return {}
        answers = get_answers(2)
        return {f"q3_{i + 1}": answers[i] for i in range(len(answers))}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        """Mark quiz as complete"""
        player.quiz3_complete = True


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
