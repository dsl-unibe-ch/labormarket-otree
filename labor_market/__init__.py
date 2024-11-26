"""Main simulation"""
from __future__ import annotations
import uuid
import random
from typing import Self, List, Optional

from otree.api import *

# Constants

class C(BaseConstants):
    """Constants for the labor_market app"""
    NAME_IN_URL = "labor_market"
    NUM_ROUNDS = 10 # Number of periods of simulation

    PLAYERS_PER_GROUP = 10
    NUM_MANAGERS = 4
    NUM_EMPLOYEES = 6
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

    HIRING_STEPS = 6 # Max number of repeated attempts at hiring (should equal number of employees)

# Name generators

class CompanyLabels(ExtraModel):
    """Random labels for Employers"""
    name = models.StringField()

class EmployeeLabels(ExtraModel):
    """Random labels for Employees"""
    name = models.StringField()

def random_labels():
    """Populates random label models"""
    company_labels = read_csv('labor_market/names/companies.csv', CompanyLabels)
    employee_labels = read_csv('labor_market/names/employees.csv', EmployeeLabels)

    return random.sample([label["name"] for label in company_labels], k=C.NUM_MANAGERS) + \
           random.sample([label["name"] for label in employee_labels], k=C.NUM_EMPLOYEES)

# Objects

class Subsession(BaseSubsession):
    """Subsession object for simulation"""

@staticmethod
def creating_session(subsession: Subsession):
    """Set per-session participant data"""
    if subsession.round_number == 1:
        if subsession.session.config["randomize_roles"]:
            subsession.group_randomly()
        for group in subsession.get_groups():
            labels = random_labels()
            for player in group.get_players():
                player.label = labels[player.id_in_group - 1]
    else:
        subsession.group_like_round(1)
        for player in subsession.get_players():
            player.label = player.in_round(1).label


class Player(BasePlayer):
    """Player object for simulation"""
    ### Player properties
    label          = models.StringField()
    skill          = models.IntegerField(initial=1)
    skill_increase = models.BooleanField(initial=False)
    offer_step     = models.IntegerField(initial=1)

    ### Form fields
    offer_employee = models.IntegerField(widget=widgets.RadioSelect)
    offer_wage     = models.CurrencyField(label="Binding wage offer (1–150)", min=1, max=150)
    offer_training = models.BooleanField(label="Include training", widget=widgets.RadioSelectHorizontal)
    work_effort    = models.IntegerField(label="Effort", min=1, max=10, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    player_matched = models.IntegerField(widget=widgets.RadioSelect, initial=0)

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
        """Returns the ID of the possible offer for a given Manager, or -1 if ineligible. Required for a combined table of eligible/ineligible employees."""
        for index, employee_id in enumerate(offer_employee_choices(manager)):
            if self.id_in_group == employee_id:
                return index
        return -1

    @property
    def contract(self) -> Optional[Offer]:
        """Return accepted offer, or return None"""
        if self.role == "Manager":
            accepted_offers = Offer.filter(manager=self, accepted=True)
        else:
            accepted_offers = Offer.filter(employee=self, accepted=True)

        if len(accepted_offers) == 1:
            return accepted_offers[0]
        elif len(accepted_offers) == 0:
            return None
        else:
            raise RuntimeError(f"Player {self.id_in_group} does not have exactly one accepted offer")

    @property
    def offer_history(self) -> List[Offer]:
        """Return a history of all offers for the participant across periods"""
        offer_history = []

        for player in self.in_rounds(1, self.round_number):
            if self.role == "Manager":
                offer_history += Offer.filter(manager=player)
            else:
                offer_history += Offer.filter(employee=player)

        return list(reversed(offer_history))


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
        ]


# Extra models

class Offer(ExtraModel):
    """An offer from manager to employee"""
    period   = models.IntegerField()
    step     = models.IntegerField()
    manager  = models.Link(Player)
    employee = models.Link(Player)
    group    = models.Link(Group)
    wage     = models.CurrencyField()
    training = models.BooleanField()
    accepted = models.BooleanField(initial=False)
    rejected = models.BooleanField(initial=False)
    effort   = models.IntegerField(initial=0)

# Pages

def stage_counter(player: Player, with_step: bool = False) -> str:
    """Formatted period + stage counter for display in titles"""
    return f"(Period { player.subsession.round_number }/{ C.NUM_ROUNDS }" + (f" | Step { player.offer_step }/{ C.HIRING_STEPS })" if with_step else ")")

class WaitForAllPlayers(WaitPage):
    """Wait page to synchronize everyone before a Period starts"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for all participants " + stage_counter(player),
            "body_text": "Please wait until all participants have entered this Period..."
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.round_number > 1:
            for player in group.get_players():
                prev_player = player.in_round(group.round_number - 1)
                player.skill = prev_player.skill
                if prev_player.skill_increase:
                    player.skill += 1

    @staticmethod
    def is_displayed(player):
        return player.offer_step == 1

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
            offers=player.offer_history
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
                period=manager.round_number,
                step=manager.offer_step
            )

class WaitForOffers(WaitPage):
    """Wait for offers page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for offers { stage_counter(player, with_step=True) }",
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
        open_offers = Offer.filter(employee=player, accepted=False, rejected=False)
        return player.role == "Employee" and player.player_matched == 0 and len(open_offers) > 0

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

class WaitForAcceptance(WaitPage):
    """Wait for acceptance page; shown to Managers without a match or Employees without a valid offer."""
    @staticmethod
    def vars_for_template(player: Player):
        if player.role == "Manager":
            return {
                "title_text": f"Waiting for offer acceptance { stage_counter(player, with_step=True) }",
                "body_text": "You are a Manager. Please wait until all Employees decide on their offers..."
            }
        else:
            return {
                "title_text": f"Waiting for offer acceptance { stage_counter(player, with_step=True) }",
                "body_text": "You are an Employee. You did not receive any offers this hiring step. Please wait until all Employees decide on their offers..."
            }


    @staticmethod
    def is_displayed(player: Player):
        open_offers = Offer.filter(employee=player, accepted=False, rejected=False)
        return (player.role == "Manager" and player.player_matched == 0) or \
            (player.role == "Employee" and player.player_matched == 0 and len(open_offers) == 0)

    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.offer_step += 1


class WaitForWork(WaitPage):
    """Wait for work page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for the work phase { stage_counter(player) }",
            "body_text": "You have a match! Please wait until the hiring phase is over for everyone..."
        }

class ChooseEffort(Page):
    """Page where employees choose how much effort to apply"""
    form_model = "player"
    form_fields = ["work_effort"]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == "Employee" and player.player_matched != 0

    @staticmethod
    def vars_for_template(employee: Player):
        return dict(
            contract=employee.contract,
            offers=Offer.filter(group=employee.group),
            effort_costs=employee.session.config["effort_costs"]
        )

    @staticmethod
    def before_next_page(employee: Player, timeout_happened: bool):
        if timeout_happened:
            print(f"Timeout for Employee {employee.id_in_group}, applying minimum effort")
            employee.work_effort = 1
        employee.contract.effort = employee.work_effort

class WaitForEffort(WaitPage):
    """Wait page for managers while employees choose effort"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for the work phase { stage_counter(player) }",
            "body_text": "Waiting for everyone to finish the work phase..."
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        """Calculate all payoffs"""
        for player in group.get_players():
            contract = player.field_maybe_none("contract")

            if player.role == "Employee":
                endowment = cu(player.session.config["employee_endowment"])

                if contract:
                    effort_cost = cu(player.session.config["effort_costs"][player.work_effort - 1])
                    print(f"Payoff for Employee {player.id_in_group}: {endowment} + {contract.wage} - {effort_cost}")
                    player.payoff = endowment + contract.wage - effort_cost
                    if contract.training:
                        player.skill_increase = True
                else:
                    print(f"Payoff for Employee {player.id_in_group}: {endowment}")
                    player.payoff = endowment
            elif player.role == "Manager":
                endowment = cu(player.session.config["manager_endowment"])

                if contract:
                    effort = contract.employee.work_effort
                    skill_multiplier = player.session.config["skill_multipliers"][contract.employee.skill - 1]
                    base_revenue = player.session.config["base_revenue"]

                    revenue = cu(round(base_revenue * skill_multiplier * effort))

                    if contract.training:
                        training_cost = cu(player.session.config["training_cost"])
                        training_productivity_multiplier = player.session.config["training_productivity_multiplier"]
                        print(f"Payoff for Manager {player.id_in_group}: {endowment} + " +
                            f"{revenue * training_productivity_multiplier} - {training_cost} - {contract.wage}"
                        )
                        player.payoff = endowment + revenue * training_productivity_multiplier \
                                        - training_cost - contract.wage
                    else:
                        print(f"Payoff for Manager {player.id_in_group}: {endowment} + {revenue} - {contract.wage}")
                        player.payoff = endowment + revenue - contract.wage
                else:
                    print(f"Payoff for Manager {player.id_in_group}: {endowment}")
                    player.payoff = endowment

class PeriodResults(Page):
    """Period outcomes display"""
    @staticmethod
    def vars_for_template(player: Player):
        if player.role == "Manager":
            offers = Offer.filter(manager=player)
            if player.field_maybe_none("contract"):
                skill_multiplier = player.session.config["skill_multipliers"][player.contract.employee.skill - 1]
                base_revenue = player.session.config["base_revenue"]
                revenue = cu(round(base_revenue * skill_multiplier * player.contract.employee.work_effort))
            else:
                skill_multiplier = 0
                revenue = cu(0)
            return {
                "offers": offers,
                "skill_multiplier": skill_multiplier,
                "revenue": revenue,
                "multiplied_revenue": revenue * player.session.config["training_productivity_multiplier"]
            }
        else:
            offers = Offer.filter(employee=player)
            if player.field_maybe_none("work_effort"):
                effort_cost = cu(player.session.config["effort_costs"][player.work_effort - 1])
            else:
                effort_cost = 0
            return {
                "offers": offers,
                "effort_cost": effort_cost
            }

page_sequence = [WaitForAllPlayers, MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * C.HIRING_STEPS + [WaitForWork, ChooseEffort, WaitForEffort, PeriodResults]
