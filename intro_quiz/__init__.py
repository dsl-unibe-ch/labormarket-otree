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
    def q_2_7_options(self):
        session = self.session
        market = session.config["market"]

        return dict(
            homoogenous_low="In the first period, all workers start with a skill level of 1.",
            homoogenous_high="In the first period, all workers start with a skill level of 5.",
            heterogenous="In the first period, three workers start with a skill level of 1 "
                         "and three workers start with a skill level of 5."
        )[market]

    skill = models.IntegerField(initial=1)

    # Quiz 1
    q_1_1 = models.BooleanField(label="This study consists of 10 periods.")
    q_1_2 = models.BooleanField(label="Each period consists of a hiring phase and a work phase.")
    q_1_3 = models.BooleanField(label="In the hiring phase of each period, each employer <strong>must</strong> "
                                          "make a contract offer to one worker.")
    q_1_4 = models.BooleanField(label="In the hiring phase of each period, workers review the offers they received "
                                          "and <strong>must</strong> accept one offer.")
    q_1_5 = models.BooleanField(label="If a worker rejects an offer received from an employer in the hiring phase "
                                          "of a period, the worker <strong>will</strong> be able to receive another "
                                          "offer <strong>from the same employer in that period</strong>.")
    q_1_6 = models.BooleanField(label="Employer offers include a salary and whether training is provided during "
                                          "the period. Regardless of the worker's effort decision during the "
                                          "subsequent work phase, the salary and training specified in the accepted "
                                          "offer must be provided.")
    q_1_7 = models.BooleanField(label="Employers and workers who do not contract in the hiring phase of a period "
                                          "receive only their initial endowment for that period and do not complete "
                                          "the work phase. Employers do not receive revenue from worker effort and "
                                          "workers do not receive a salary from an employer.")
    q_1_8 = models.BooleanField(label="In the work phase of each period, every hired worker must decide how much "
                                          "effort to exert. Higher levels of effort are <strong>more costly</strong> "
                                          "to the worker than lower levels of effort.")
    q_1_9 = models.BooleanField(label="For every worker skill level, the higher the level of effort a worker "
                                          "chooses, the higher an employer's revenue is.")
    q_1_10 = models.BooleanField(label="Worker's productivity is based on his/her skill level. The higher the "
                                           "worker's skill level, the higher the worker's productivity is and, thus, "
                                           "the higher the revenue for the employer is for a given effort level.")
    q_1_11 = models.BooleanField(label="In the hiring phase in <strong>each</strong> of the 10 periods, every "
                                           "employer can again select <strong>any</strong> potential worker to make a "
                                           "contract offer to and every worker can freely accept one of the contract "
                                           "offers they receive.")

    # Quiz 2
    q_2_1 = models.BooleanField(label="If an employer provides training to a worker, he/she incurs a 50-point direct "
                                      "training cost.")
    q_2_2 = models.BooleanField(label="Providing training to workers is costly to employers not only because the "
                                      "employer incurs a direct training cost of 50 points, but also because in "
                                      "a period with training the employer will only receive half of the revenue "
                                      "that is generated by the combination of the worker’s skill level and "
                                      "the effort level chosen.")
    q_2_3 = models.BooleanField(label="Receiving training is costly for workers.")
    q_2_4 = models.BooleanField(label="If a worker receives training, his/her skill level will not increase until "
                                      "the following period.")
    q_2_5 = models.BooleanField(label="Increases in skill level are permanent and apply to all future periods.")
    q_2_6 = models.BooleanField(label="When workers receive training in a period, they <strong>do not</strong> make "
                                      "effort decisions in the work phase like they would if training was not "
                                      "provided.")
    q_2_7 = models.BooleanField(label=q_2_7_options)
    q_2_8 = models.BooleanField(label=f"Your skill level in the first period is <strong>{skill}</strong>.")


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


def prepare_error_message(correct_answer):
    return f"Your response is incorrect. {correct_answer} Please try again."


# Error messages for questions

def q_1_1_error_message(player, value):
    if not value:
        return prepare_error_message("This study consists of 10 periods.")
    else:
        return None

def q_1_2_error_message(player, value):
    if not value:
        return prepare_error_message("Each period consists of a hiring phase and a work phase.")
    else:
        return None

def q_1_3_error_message(player, value):
    if value:
        return prepare_error_message("Each employer does not have to make a contract offer to a worker.")
    else:
        return None

def q_1_4_error_message(player, value):
    if value:
        return prepare_error_message("Workers do not have to accept an offer.")
    else:
        return None

def q_1_5_error_message(player, value):
    if value:
        return prepare_error_message("If a worker rejects an offer received from an employer in the hiring phase of a "
                                     "period, the worker will not be able to receive another offer from the same "
                                     "employer in that period.")
    else:
        return None

def q_1_6_error_message(player, value):
    if not value:
        return prepare_error_message("Employer offers include a salary and whether training is provided during the "
                                     "period. The specified salary and training must be provided.")
    else:
        return None

def q_1_7_error_message(player, value):
    if not value:
        return prepare_error_message("Employers and workers who do not contract do not receive revenue from worker "
                                     "effort or a salary respectively.")
    else:
        return None

def q_1_8_error_message(player, value):
    if not value:
        return prepare_error_message("Every hired worker must decide how much effort to exert. Higher levels of "
                                     "effort are more costly to them.")
    else:
        return None

def q_1_9_error_message(player, value):
    if not value:
        return prepare_error_message("The higher the level of effort a worker chooses, the higher an employer's "
                                     "revenue is.")
    else:
        return None

def q_1_10_error_message(player, value):
    if not value:
        return prepare_error_message("Worker's productivity is based on his/her skill level. The higher the "
                                     "worker's skill level, the higher the worker's productivity is and, thus, "
                                     "the higher the revenue for the employer is for a given effort level.")
    else:
        return None

def q_1_11_error_message(player, value):
    if not value:
        return prepare_error_message("In the hiring phase in each of the 10 periods, every employer can again "
                                     "select any potential worker to make a contract offer to and every worker can "
                                     "freely accept one of the contract offers they receive.")
    else:
        return None

def q_2_1_error_message(player, value):
    if not value:
        return prepare_error_message("The employer incurs a 50-point direct training cost.")
    else:
        return None

def q_2_2_error_message(player, value):
    if not value:
        return prepare_error_message("In a period with training the employer will only receive half of the revenue "
                                     "that would have been generated without the training.")
    else:
        return None

def q_2_3_error_message(player, value):
    if value:
        return prepare_error_message("")
    else:
        return None

def q_2_4_error_message(player, value):
    if not value:
        return prepare_error_message("The skill level will not increase until the following period.")
    else:
        return None

def q_2_5_error_message(player, value):
    if not value:
        return prepare_error_message("Increases in skill level are permanent.")
    else:
        return None

def q_2_6_error_message(player, value):
    if value:
        return prepare_error_message("")
    else:
        return None

def q_2_7_error_message(player, value):
    if not value:
        return prepare_error_message(player.q_2_7_options)
    else:
        return None

def q_2_8_error_message(player, value):
    if not value:
        return prepare_error_message(f"Your skill level in the first period is <strong>{player.skill}</strong>.")
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
            group=dir(player.group),
            worker_info=f"Your skill level in the first period is {player.skill}."
                    if player.role == "Employee" else None
        )


class Instructions6(Page):
    """Intro page with instructions"""


class Quiz1(Page):
    """Quiz page to test comprehension"""
    form_model = "player"
    form_fields = ["q_1_1", "q_1_2", "q_1_3", "q_1_4", "q_1_5", "q_1_6", "q_1_7", "q_1_8", "q_1_9", "q_1_10", "q_1_11"]


class Quiz2(Page):
    """Quiz page to test comprehension"""
    form_model = "player"
    form_fields = ["q_2_1", "q_2_2", "q_2_3", "q_2_4", "q_2_5", "q_2_6", "q_2_7", "q_2_8"]

    @staticmethod
    def vars_for_template(player: Player):
        """Providing variables for template"""
        session = player.session

        return dict(
            player=dir(player),
            player_skill=player.skill,
            player_role=player.role,
            session=dir(session),
        )


# TODO: The skills and roles should be transferred to the next app
def creating_session(subsession: Subsession):
    """Set per-session participant data"""
    # In the first Period, set labels and reshuffle participants
    if subsession.round_number == 1:
        # If session config dictates, reshuffle participants randomly
        if subsession.session.config["randomize_roles"]:
            subsession.group_randomly()
        for group in subsession.get_groups():
            # Set initial skills according to session config
            for index, player in enumerate(group.employees):
                player.skill = subsession.session.config["starting_skills"][index]


# page_sequence = [Consent, Instructions1, Instructions2, Instructions3, Quiz1, Instructions4, Instructions5,
#                  Instructions6]
page_sequence = [Instructions4, Instructions5,
                 Instructions6, Quiz2]
