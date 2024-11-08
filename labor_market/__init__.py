"""Main simulation"""
import uuid
import random
from typing import Self, List

from otree.api import *

# Constants

class C(BaseConstants):
    """Constants for the labor_market app"""
    NAME_IN_URL = "labor_market"
    NUM_ROUNDS = 10

    PLAYERS_PER_GROUP = 10
    MANAGER1_ROLE = "Manager"
    MANAGER2_ROLE = "Manager"
    MANAGER3_ROLE = "Manager"
    MANAGER4_ROLE = "Manager"
    EMPLOYEE1_ROLE = "Employee"
    EMPLOYEE2_ROLE = "Employee"
    EMPLOYEE3_ROLE = "Employee"
    EMPLOYEE4_ROLE = "Employee"
    EMPLOYEE5_ROLE = "Employee"
    EMPLOYEE6_ROLE = "Employee"

    HIRING_STEPS = 6

# Objects

class Subsession(BaseSubsession):
    """Subsession object for simulation"""

@staticmethod
def creating_session(subsession: Subsession):
    """Set per-session participant data"""
    if subsession.round_number == 1:
        if subsession.session.config["randomize_roles"]:
            subsession.group_randomly()
        for player in subsession.get_players():
            player.set_random_label()
    else:
        subsession.group_like_round(1)
        for player in subsession.get_players():
            player.label = player.in_round(1).label


class Player(BasePlayer):
    """Player object for simulation"""
    ### Player properties
    label          = models.StringField()
    skill          = models.IntegerField(initial=1)
    offer_step     = models.IntegerField(initial=1)

    ### Form fields
    offer_employee = models.IntegerField(widget=widgets.RadioSelect)
    offer_wage     = models.CurrencyField(label="Binding wage offer (1–150)", min=1, max=150)
    offer_training = models.BooleanField(label="Include training", widget=widgets.RadioSelectHorizontal)


    player_matched = models.IntegerField(widget=widgets.RadioSelect, initial=0)

    def set_random_label(self):
        """Sets label to a random one"""
        self.label = str(uuid.uuid4())

    @property
    def is_hired(self) -> bool:
        """Returns True/False whether the Employee player accepted an offer"""
        return len(Offer.filter(employee=self, accepted=True)) > 0

    @property
    def has_hired(self) -> bool:
        """Returns True/False whether the Manager player hired an Employee"""
        return len(Offer.filter(employee=self, accepted=True)) > 0

    def rejected_from(self, manager: Self) -> bool:
        """Returns True/False whether the Employee player rejected an offer from a given Manager"""
        return len(Offer.filter(employee=self, manager=manager, rejected=True)) > 0

    def choice_id(self, manager: Self) -> int:
        """Returns the ID of the possible offer for a given Manager, or -1 if ineligible. Required for a combined table of eligible/ineligible workers."""
        for index, employee_id in enumerate(offer_employee_choices(manager)):
            if self.id_in_group == employee_id:
                return index
        return -1


def offer_employee_choices(manager: Player):
    """Dynamically provide employee choices"""
    employee_ids = [employee.id_in_group for employee in manager.group.for_hire(manager)]
    return employee_ids

def player_matched_choices(employee: Player):
    """Dynamically provide offer choices"""
    open_offers = Offer.filter(employee=employee, accepted=False, rejected=False)
    manager_ids = [offer.manager.id_in_group for offer in open_offers]

    return manager_ids + [0] # It's always possible to reject offers with 0

class Group(BaseGroup):
    """Group object for simulation"""

    @property
    def managers(self):
        """Return all Manager players from the current group"""
        return [player for player in self.get_players() if player.role == "Manager"]

    @property
    def employees(self) -> List[Player]:
        """Return all Employee players from the current group"""
        return [player for player in self.get_players() if player.role == "Employee"]

    def for_hire(self, manager):
        """Return all Employee players still open for offer"""
        if self is not manager.group:
            raise RuntimeError("Trying to hire from wrong group!")

        # Rejected binding offers
        my_offers_rejected = Offer.filter(manager=manager, rejected=True)

        return [
            employee
            for employee in self.employees                                        # Check all employees in the group
            if not employee.player_matched                                        # Must not have an accepted employer
            and employee not in (offer.employee for offer in my_offers_rejected)  # Must not have rejected manager's offer
            and employee.id_in_group > 6                                          # TEST ONLY: make first 2 employees ineligible
        ]


# Extra models

class Offer(ExtraModel):
    """An offer from manager to employee"""
    round    = models.IntegerField()
    step     = models.IntegerField()
    manager  = models.Link(Player)
    employee = models.Link(Player)
    group    = models.Link(Group)
    wage     = models.CurrencyField()
    training = models.BooleanField()
    accepted = models.BooleanField(initial=False)
    rejected = models.BooleanField(initial=False)

# Pages

def stage_counter(player: Player) -> str:
    """Formatted round + stage counter for display in titles"""
    return f"(Round { player.subsession.round_number }/{ C.NUM_ROUNDS } | Step { player.offer_step }/{ C.HIRING_STEPS })"

class MakeOffer(Page):
    """Hiring phase page"""
    form_model = "player"
    form_fields = ["offer_employee", "offer_wage", "offer_training"]

    @staticmethod
    def vars_for_template(player):
        employee_pool = [ {
            "employee": employee,
            "rejected": employee.rejected_from(player),
            "eligible": employee.choice_id(player) >= 0,
            "choice_id": employee.choice_id(player)
        } for employee in player.group.employees ]

        return dict(
            employee_pool=employee_pool,
            offers=Offer.filter(group=player.group)
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.role == "Manager" and \
               player.player_matched == 0 and \
               len(player.group.for_hire(player)) > 0

    @staticmethod
    def before_next_page(manager: Player, timeout_happened: bool):
        if timeout_happened:
            print(f"Timeout for Manager {manager.id_in_group}, not putting forward any offers")
        else:
            employee = manager.group.get_player_by_id(manager.offer_employee)
            Offer.create(
                manager=manager,
                employee=employee,
                group=manager.group,
                wage=manager.offer_wage,
                training=manager.offer_training,
                round=manager.round_number,
                step=manager.offer_step
            )
        manager.offer_step += 1

class WaitForOffers(WaitPage):
    """Wait for offers page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for offers { stage_counter(player) }",
            "body_text": "You are an Employee. Please wait until all managers have made their offers..."
        }

    @staticmethod
    def is_displayed(player):
        return player.role == "Employee" and player.player_matched == 0


class GetOffers(Page):
    """Hiring phase page"""
    form_model = "player"
    form_fields = ["player_matched"]

    @staticmethod
    def vars_for_template(player: Player):
        open_offers = Offer.filter(employee=player, accepted=False, rejected=False)
        return dict(
            open_offers=open_offers,
            num_offers=len(open_offers),
            offers=Offer.filter(group=player.group)
        )

    @staticmethod
    def is_displayed(player):
        return player.role == "Employee" and player.player_matched == 0

    @staticmethod
    def before_next_page(employee: Player, timeout_happened: bool):
        if timeout_happened:
            print(f"Timeout for Employee {employee.id_in_group}, not accepting any offers")
        elif employee.player_matched > 0:
            manager = employee.group.get_player_by_id(employee.player_matched)
            manager.player_matched = employee.id_in_group

            offers = Offer.filter(manager=manager, employee=employee, accepted=False, rejected=False)
            assert len(offers) == 1
            accepted_offer = offers[0]

            accepted_offer.accepted = True
            employee.offer_wage = accepted_offer.wage
            employee.offer_training = accepted_offer.training

        open_offers = Offer.filter(employee=employee, accepted=False, rejected=False)
        for offer in open_offers:
            offer.rejected = True

        employee.offer_step += 1

class WaitForAcceptance(WaitPage):
    """Wait for acceptance page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for offer acceptance { stage_counter(player) }",
            "body_text": "You are a Manager. Please wait until all Employees decide on their offers..."
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.role == "Manager" and player.player_matched == 0

class WaitForWork(WaitPage):
    """Wait for work page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for the work phase { stage_counter(player) }",
            "body_text": "You have a match! Please wait until the hiring phase is over for everyone..."
        }

page_sequence = [MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * C.HIRING_STEPS + [WaitForWork]
