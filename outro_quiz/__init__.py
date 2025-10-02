"""Initial outro with rules and quiz"""
from typing import Iterator, List

from otree.api import *
from otree.currency import RealWorldCurrency

from . import nodes_extra

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
    MANAGER4_ROLE = "Manager"
    MANAGER5_ROLE = "Manager"
    MANAGER6_ROLE = "Manager"
    EMPLOYEE1_ROLE = "Employee"
    EMPLOYEE2_ROLE = "Employee"
    EMPLOYEE3_ROLE = "Employee"
    EMPLOYEE4_ROLE = "Employee"
    EMPLOYEE5_ROLE = "Employee"
    EMPLOYEE6_ROLE = "Employee"

    LIKERT_SCALE_DISAGREE_AGREE = { 1: "Strongly disagree", 2: "", 3: "", 4:"", 5: "", 6: "", 7: "Strongly agree" }
    LIKERT_SCALE_LOWER_HIGHER = { -3: "Much lower", -2: "", -1: "", 0: "The same", 1: "", 2: "", 3: "Much higher" }
    LIKERT_SCALE_WORSE_BETTER = { -3: "Much worse than expected", -2: "", -1: "", 0: "Exactly as expected",
                                  1: "", 2: "", 3: "Much better than expected" }
    LIKERT_SCALE_RISK = { 1: "Completely risk averse", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
                         10: "Completely risk seeking" }

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
            if player.role == "Employee":
                yield [
                    player.participant.code,
                    player.e_peq_quiz1,
                    player.e_peq_quiz2,
                    player.e_peq_quiz3,
                    player.e_peq_quiz4,
                    player.e_peq_quiz5,
                    player.e_peq_quiz6,
                    player.e_peq_quiz7,
                    player.e_peq_quiz8,
                    player.e_peq_quiz9,
                    player.e_peq_quiz10,
                    player.e_peq_quiz11,
                    player.e_peq_quiz12,
                    player.e_peq_quiz13,
                    player.e_peq_quiz14,
                    player.e_peq_quiz15,
                    player.e_peq_quiz16,
                    player.e_peq_quiz17,
                    player.demographic_quiz1,
                    player.demographic_quiz2,
                    player.demographic_quiz3,
                    player.demographic_quiz4,
                    player.demographic_quiz5,
                    player.demographic_quiz6,
                    player.demographic_quiz7,
                    player.demographic_quiz8,
                ]
            else:
                yield [
                    player.participant.code,
                    player.m_peq_quiz1,
                    player.m_peq_quiz2,
                    player.m_peq_quiz3,
                    player.m_peq_quiz4,
                    player.m_peq_quiz5,
                    player.m_peq_quiz6,
                    player.m_peq_quiz7,
                    player.m_peq_quiz8,
                    player.m_peq_quiz9,
                    player.m_peq_quiz10,
                    player.m_peq_quiz11,
                    player.m_peq_quiz12,
                    player.m_peq_quiz13,
                    player.m_peq_quiz14,
                    player.m_peq_quiz15,
                    player.m_peq_quiz16,
                    player.m_peq_quiz17,
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


@staticmethod
def creating_session(subsession: Subsession):
    """Set per-session participant data"""

    # In the first Period, set labels and reshuffle participants
    if subsession.round_number == 1:
        if "frozen_matrix" in subsession.session.vars:
            # If we had the players set from the previous app, use it
            subsession.set_group_matrix(subsession.session.vars["frozen_matrix"])
        else:
            # If session config dictates, reshuffle participants randomly
            if subsession.session.config["randomize_roles"]:
                subsession.group_randomly()

        for group in subsession.get_groups():
            # Set initial skills according to session config. This should be the same regardless of whether
            # this is the first app or not.
            for index, player in enumerate(group.employees):
                player.skill = subsession.session.config["starting_skills"][index]
    else:
        # In subsequent Periods, retain the same group/role and labels
        subsession.group_like_round(1)
        for player in subsession.get_players():
            player.label = player.in_round(1).label


class Player(BasePlayer):
    """Player object for quiz"""

    e_peq_quiz1 = models.IntegerField(label="1. <strong>I trusted the employer I formed a contract with.</strong>",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz2 = models.IntegerField(label="2. I wanted to treat the employer I formed a contract with fairly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz3 = models.IntegerField(label="3. I cared about the employer I formed a contract with.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz4 = models.IntegerField(label="4. I felt the employer I formed a contract with trusted me.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz5 = models.IntegerField(label="5. I felt the employer I formed a contract with treated me fairly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz6 = models.IntegerField(label="6. I felt the employer I formed a contract with cared about me.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz7 = models.IntegerField(label="7. I felt the employer I formed a contract with treated me kindly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz8 = models.IntegerField(label="8. I wanted to repay the kindness of the employer I formed a contract "
                                         "with.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz9 = models.IntegerField(label="9. Employers who offered training to workers trusted the workers to come "
                                         "back in future periods.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz10 = models.IntegerField(label="10. When I chose a contract including training, I felt obligated "
                                          "to return to that employer in the following periods.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz11 = models.IntegerField(label="11. I valued being offered a high <strong>salary</strong> "
                                          "by the employer.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz12 = models.IntegerField(label="12. I valued being offered <strong>training</strong> by the employer.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz13 = models.IntegerField(label="13. How would you compare the <strong>actual salary</strong> offers "
                                          "you received to the <strong>salary</strong> offers you "
                                          "<strong>expected</strong> to receive?",
                                   choices=list(C.LIKERT_SCALE_LOWER_HIGHER.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz14 = models.IntegerField(label="14. How would you compare the <strong>actual</strong> frequency "
                                          "with which you were offered <strong>training</strong> to the "
                                          "frequency with which you <strong>expected</strong> to be offered "
                                          "<strong>training</strong>?",
                                   choices=list(C.LIKERT_SCALE_LOWER_HIGHER.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz15 = models.IntegerField(label="15. When a manager offered me training in a period, the manager "
                                          "expected me to <strong>provide high effort in this period</strong>.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz16 = models.IntegerField(label="16. When a manager offered me training in a period, the manager "
                                          "expected me to <strong>contract with him or her again in the next "
                                          "period</strong>.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    e_peq_quiz17 = models.IntegerField(label="17. A worker's skill level should play a major role for the amount "
                                          "of salary an employer offers to this worker.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz1 = models.IntegerField(label="<strong>1. I trusted the worker I formed a contract with.</strong>",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz2 = models.IntegerField(label="2. I wanted to treat the worker I formed a contract with fairly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz3 = models.IntegerField(label="3. I cared about the worker I formed a contract with.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz4 = models.IntegerField(label="4. I felt the worker I formed a contract with trusted me.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz5 = models.IntegerField(label="5. I felt the worker I formed a contract with treated me fairly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz6 = models.IntegerField(label="6. I felt the worker I formed a contract with cared about me.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz7 = models.IntegerField(label="7. I felt the worker I formed a contract with treated me kindly.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz8 = models.IntegerField(label="8. When I offered training to workers, I trusted the workers to come back "
                                         "in future periods.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz9 = models.IntegerField(label="9. Workers valued being offered a high <strong>salary</strong>.",
                                   choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                   widget=widgets.RadioSelectHorizontal,
                                   blank=False)
    m_peq_quiz10 = models.IntegerField(label="10. Workers valued being offered <strong>training</strong>.",
                                    choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz11 = models.IntegerField(label="11. When a worker chose a contract including training, he/she felt "
                                          "obligated to return to that employer in the next period.",
                                    choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz12 = models.IntegerField(label="12. How would you compare the <strong>actual</strong> workers' "
                                          "<strong>effort levels</strong> to the <strong>effort levels</strong> "
                                          "you <strong>expected</strong> the workers to provide?",
                                    choices=list(C.LIKERT_SCALE_LOWER_HIGHER.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz13 = models.IntegerField(label="13. When I offered training to a worker in a period, I expected this "
                                          "worker to <strong>provide high effort in this period</strong>.",
                                    choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz14 = models.IntegerField(label="14. When I offered training to a worker in a period, I expected this "
                                          "worker to <strong>contract with me again in the next period</strong>.",
                                    choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz15 = models.IntegerField(label="15. <strong>For the periods in which the workers' contracts included "
                                          "training</strong>, how would you compare the actual workers' effort "
                                          "levels to the effort levels you expected the workers to provide?",
                                    choices=list(C.LIKERT_SCALE_LOWER_HIGHER.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz16 = models.IntegerField(label="16. <strong>For the periods in which the workers' contracts included "
                                          "training</strong>, how would you compare the actual workers' behavior "
                                          "in the next period to the behavior you expected from them in the next "
                                          "period?",
                                    choices=list(C.LIKERT_SCALE_WORSE_BETTER.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)
    m_peq_quiz17 = models.IntegerField(label="17. A worker's skill level should play a major role for the "
                                          "salary level an employer offers to this worker.",
                                    choices=list(C.LIKERT_SCALE_DISAGREE_AGREE.items()),
                                    widget=widgets.RadioSelectHorizontal,
                                    blank=False)

    demographic_quiz1 = models.StringField(
        choices=["Female", "Male", "Non-binary", "Prefer not to answer"],
        widget=widgets.RadioSelect,
        blank=False,
    )
    demographic_quiz2 = models.IntegerField(min=18, max=99, blank=False)
    demographic_quiz3 = models.StringField(
        choices=["Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
        widget=widgets.RadioSelect,
        blank=False,
    )
    demographic_quiz4 = models.StringField(max_length=50, blank=False)
    demographic_quiz5 = models.FloatField(min=0, max=5, blank=False)
    demographic_quiz6 = models.IntegerField(min=0, max=20, blank=False)
    demographic_quiz7 = models.IntegerField(choices=list(C.LIKERT_SCALE_RISK.items()),
                                            widget=widgets.RadioSelectHorizontal, blank=False)
    demographic_quiz8 = models.LongStringField(blank=False)

    @property
    def peq_quiz(self, index1):
        getattr(self, f"peq_quiz{index1}")

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

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions_count=17)

    @staticmethod
    def get_form_fields(player):
        return [f"{player.role[0].lower()}_peq_quiz{i}" for i in range(1, 18)]


class DemographicQuiz(Page):
    form_model = "player"
    form_fields = [f"demographic_quiz{i}" for i in range(1, 9)]

    @staticmethod
    def js_vars(player: "Player"):
        return dict(questions_count=8)


class Conclusion(Page):

    @staticmethod
    def vars_for_template(player: "Player"):
        session = player.session
        participation_fee = RealWorldCurrency(session.config["participation_fee"])
        real_world_currency_per_point = session.config["real_world_currency_per_point"]

        # Here we have to prevent theoretically possible negative values, otherwise the participants will owe money.
        real_payoff = max(player.participant.payoff, cu(0)).to_real_world_currency(session)
        total_payment = real_payoff + participation_fee

        return dict(real_world_currency_per_hundred_points=real_world_currency_per_point * 100,
                    participation_fee=participation_fee,
                    real_payoff=real_payoff, total_payment=total_payment)


page_sequence = [PEQ, DemographicQuiz, Conclusion]