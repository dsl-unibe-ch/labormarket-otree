"""Main simulation"""
from __future__ import annotations

import random
from collections import defaultdict
from functools import partial
from itertools import chain
from typing import Self, List, Optional, Any, Iterator
from pathlib import Path

from otree.api import *

from agent.agent import Agent
from agent.config import get_agent_settings, should_use_agent
from .agent_policy import make_agent_offer, get_agent_offer, choose_agent_effort
from .game_state import build_make_offer_state, build_get_offers_state, build_choose_effort_state

# Constants

class C(BaseConstants):
    """Constants for the labor_market app"""
    NAME_IN_URL = "labor_market"
    NUM_ROUNDS = 10 # Number of periods of simulation

    PLAYERS_PER_GROUP = 12
    NUM_MANAGERS = 6
    NUM_EMPLOYEES = 6

    # "Magic" constants (ending with _ROLE) for OTree to instantiate roles
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

    # Used in the page sequence
    HIRING_STEPS = NUM_EMPLOYEES # Max number of repeated attempts at hiring (should equal number of employees)

# Name generators

class CompanyLabels(ExtraModel):
    """Random labels for Manager companies"""
    name = models.StringField()

class EmployeeLabels(ExtraModel):
    """Random labels for Employees"""
    name = models.StringField()

def random_labels():
    """Returns a random sample of company/employee labels"""
    company_labels = read_csv("labor_market/names/companies.csv", CompanyLabels)
    employee_labels = read_csv("labor_market/names/employees.csv", EmployeeLabels)

    return random.sample([label["name"] for label in company_labels], k=C.NUM_MANAGERS) + \
           random.sample([label["name"] for label in employee_labels], k=C.NUM_EMPLOYEES)

def custom_export(players) -> Iterator[List[str]]:
    # Header row
    yield ([
               "labor_market.session_id",
               "labor_market.player.id_in_group",
               "labor_market.player.role",
               "labor_market.player.label",
               "labor_market.player.participant_code",
           ] +
           [
               header
               for period in range(1, C.NUM_ROUNDS + 1)
                   for header in ([f"labor_market.player.employee_skill.{period}"] +
                             [f"{name}.{period}.{step}"
                              for step in range(1, C.HIRING_STEPS + 1)
                              for name in ["labor_market.player.offer_decision",
                                           "labor_market.player.offer_employee",
                                           "labor_market.player.offer_wage",
                                           "labor_market.player.offer_training",
                                           "labor_market.player.employee_offer_count",
                                           "labor_market.player.offer_accept"]
                              ] +
                             [f"labor_market.player.counterparty.{period}",
                              f"labor_market.player.contract_wage.{period}",
                              f"labor_market.player.contract_training.{period}",
                              f"labor_market.player.work_effort.{period}",
                              f"labor_market.player.employee_earnings.{period}",
                              f"labor_market.player.manager_earnings.{period}",
                              f"labor_market.player.worker_costofeffort.{period}",
                              f"labor_market.player.worker_productivity.{period}"])
          ] + ["labor_market.player.participant_payoff"])
    grouped_players = defaultdict(list)

    for player in players:
        grouped_players[player.session.id].append(player)

    sorted_grouped_players = [grouped_players[session_id] for session_id in sorted(grouped_players)]

    for session_players in sorted_grouped_players:
        yield from export_for_session_players(session_players)


def export_for_session_players(session_players: list[Any]):
    session_players_last_period = [player for player in session_players if player.round_number == C.NUM_ROUNDS]

    for final_player in session_players_last_period:
        result = [
            final_player.session.code,
            final_player.id_in_group,
            final_player.role,
            final_player.label,
            final_player.participant.code
        ]

        players_in_all_periods = final_player.in_all_rounds()

        # Get all offers from the database once, to avoid too many queries
        player_offers: List[Offer] = []
        for player_in_period in players_in_all_periods:
            player_offers += Offer.filter(manager=player_in_period) if player_in_period.role == "Manager" \
                else Offer.filter(employee=player_in_period)

        for player_in_period in players_in_all_periods:
            result += [
                item
                for item in [get_player_skill(player_in_period)] + get_hiring_data(player_in_period, player_offers) +
                            get_work_data(player_in_period, player_offers)
            ]
        
        result += [final_player.participant.payoff]

        yield result


# Helper methods

def get_player_skill(player: Player) -> str:
    if player.role == "Employee":
        return str(player.skill)
    else:
        return ""

def get_work_data(player: Player, player_offers: List[Offer]) -> List[str]:
    config = player.session.config
    contracts: List[Offer] = [offer for offer in player_offers if offer.accepted and offer.period == player.round_number]

    if len(contracts) > 0:
        contract: Offer = contracts[0]

        if contract.effort:
            return [
                str(contract.manager.id_in_group if player.role == "Employee" else contract.employee.id_in_group), # Counterparty
                str(int(contract.wage)),
                str(bool_to_int(contract.training)),
                str(contract.effort),
                str(contract.employee_earnings),
                str(contract.manager_earnings),
                str(config["effort_costs"][contract.effort - 1]),
                str(config["skill_multipliers"][contract.employee.skill - 1])
            ]
        else:
            # This should only happen if the session was incomplete
            return [
                str(contract.manager.id_in_group if player.role == "Employee" else contract.employee.id_in_group), # Counterparty
                str(int(contract.wage)),
                str(bool_to_int(contract.training)),
                "N/A",
                "N/A",
                "N/A",
                "N/A",
                "N/A"
            ]
    else:
        return [""] * 8

def get_hiring_data(player: Player, player_offers: List[Offer]) -> List[str]:
    f = partial(get_hiring_data_for_step, player, player_offers)
    return list(chain.from_iterable(map(f, range(1, C.HIRING_STEPS + 1))))

def manager_offered_none_on_step(manager: Player, player_offers: List[Offer], step: int) -> bool:
    # Offered none if no offers are in current step, but they were in the previous step (if it exists).
    # There should not be an accepted contract in the previous step.
    if any(offer.accepted for offer in player_offers if offer.manager == manager and offer.period == manager.round_number):
        return False
    return len([offer for offer in player_offers if offer.manager == manager and offer.period == manager.round_number and offer.step == step]) == 0

def get_hiring_data_for_step(player: Player, player_offers: List[Offer], step: int) -> List[str]:
    offers: List[Offer] = [offer for offer in player_offers if offer.period == player.round_number and offer.step == step]

    offer_count = len(offers)
    if offer_count > 0:
        # If at least one offer exists

        if player.role == "Manager":
            # Managers can have only one offer
            offer: Offer = offers[0]

            # if not manager_offer_none:
            manager_result = [
                "1",
                str(offer.employee.id_in_group),
                str(int(offer.wage)),
                str(bool_to_int(offer.training))
            ]
            employee_result = [""]
        else:
            manager_result = [""] * 4
            employee_result = [str(offer_count)]

        # Add the information if an offer has been accepted
        return manager_result + employee_result + [str(bool_to_int(any(offer.accepted for offer in offers)))]
    else:
        # If there is no offer in this period and step.
        # The locations of zeroes and empty values are different to managers and employees
        if player.role == "Manager":
            return ["0" if manager_offered_none_on_step(player, player_offers, step) else ""] + ["0"] * 3 + ["", "0"]
        else:
            return [""] * 4 + ["0", "0"]


def bool_to_int(b: bool) -> int:
    return 1 if b else 0

def calculate_manager_revenue_and_payoff(group: Group, player: BasePlayer, revenue: cu | int, wage: int,
                                         has_training: bool) -> dict[str, cu | int]:
    config = group.session.config
    endowment: int = config["manager_endowment"]
    if has_training:
        training_cost = config["training_cost"]
        training_productivity_multiplier = config["training_productivity_multiplier"]
        return {
            "message": (f"Payoff for Employer {player.id_in_group}: {endowment} + "
                          f"{revenue * training_productivity_multiplier} - {training_cost} - {wage}"),
            "payoff": endowment + revenue * training_productivity_multiplier - training_cost - wage,
            "revenue": revenue * training_productivity_multiplier - training_cost
        }
    else:
        return {
            "message": f"Payoff for Manager {player.id_in_group}: {endowment} + {revenue} - {wage}",
            "payoff": endowment + revenue - wage,
            "revenue": revenue
        }

def multiplier_to_table_item(mult_tuple: tuple[int, int]):
    """Prepare multiplier table for template"""
    index, multiplier = mult_tuple

    return {
        "level": index + 1,
        "multiplier": multiplier,
        "revenue": [effort * multiplier for effort in range(1, 11)] # TODO make 1 configurable through base_revenue
    }

# Objects

def calculate_employee_payoff(endowment: int, wage: int, effort_cost: int) -> int:
    return endowment + wage + effort_cost

class Subsession(BaseSubsession):
    """Subsession object for simulation"""
    @property
    def skill_table(self):
        """Prepare skill table for template"""
        return list(map(
            multiplier_to_table_item,
            enumerate(self.session.config["skill_multipliers"])
        ))

    @property
    def skill_distribution(self):
        """Human-readable description of the skill distribution"""
        counts = {}
        for skill in self.session.config["starting_skills"]:
            counts[skill] = counts.get(skill, 0) + 1
        return ", ".join([f"{counts[skill]} Worker(s) with Skill level {skill}" for skill in counts.keys()])

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

            group_matrix = subsession.get_group_matrix()
            print(f"Group matrix: {group_matrix}")
            subsession.session.vars["frozen_matrix"] = group_matrix

        for group in subsession.get_groups():
            # Set random labels (company names for Managers, nicknames for Employees)
            labels = random_labels()
            for player in group.get_players():
                player.label = labels[player.id_in_group - 1]
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
    """Player object for simulation"""
    ### Player properties
    # Visible "name" for the player (company name or employee nickname)
    label             = models.StringField()
    # Skill level
    skill             = models.IntegerField(initial=1)
    # Whether the skill should increase in the next Period (skill level remains constant inside a Period)
    skill_increase    = models.BooleanField(initial=False)
    # Current hiring phase step
    offer_step        = models.IntegerField(initial=1)
    # Whether the payoff is already calculated for the Period
    payoff_calculated = models.BooleanField(initial=False)

    ### Form fields

    ## Managers
    # Which employee to make an offer to
    offer_employee    = models.IntegerField(widget=widgets.RadioSelect)
    # What wage to include in the offer
    # Max is set up programmatically in offer_wage_max()
    # Label is set up programmatically in the form template
    offer_wage        = models.CurrencyField(label="Binding wage offer", min=1)
    # Whether to include training in the offer
    offer_training    = models.BooleanField(label="Include training?", widget=widgets.RadioSelectHorizontal)
    # Whether the Manager decided to have no more offers
    offer_none        = models.BooleanField(initial=False)

    ## Employees
    # Whose offer to accept (or 0 if rejecting all)
    # This field is also set for the manager to point at the employee when offer is accepted.
    player_matched    = models.IntegerField(widget=widgets.RadioSelect, initial=0)
    # What level of effort to exert
    work_effort       = models.IntegerField(label="Effort", min=1, max=10, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def rejected_from(self, manager: Self) -> bool:
        """Returns True/False whether the Employee player rejected an offer from a given Manager"""
        return len(Offer.filter(employee=self, manager=manager, rejected=True)) > 0

    def choice_id(self, manager: Self) -> int:
        """Returns the ID of the possible offer for a given Manager, or -1 if ineligible. Required for a combined table of eligible/ineligible employees."""
        for index, employee_id in enumerate(offer_employee_choices(manager)):
            if self.id_in_group == employee_id:
                return index
        return -1

    def for_hire(self):
        """Return all Employee players still open for offer from this manager"""
        # Rejected binding offers
        my_offers_rejected = Offer.filter(manager=self, rejected=True)

        return [
            employee
            for employee in self.group.employees                                  # Check all employees in the group
            if not employee.player_matched                                        # Must not have an accepted employer
            and employee not in (offer.employee for offer in my_offers_rejected)  # Must not have rejected manager's offer
        ]

    @property
    def contract(self) -> Optional[Offer]:
        """Return accepted Offer, or return None"""
        if self.role == "Manager":
            accepted_offers = Offer.filter(manager=self, accepted=True)
        else:
            accepted_offers = Offer.filter(employee=self, accepted=True)

        if len(accepted_offers) == 1:
            return accepted_offers[0]
        if len(accepted_offers) == 0:
            return None

        raise RuntimeError(f"Player {self.id_in_group} does not have exactly one accepted offer")

    def get_offers_last_round(self) -> Iterator[Offer]:
        """Yield all (non-open) offers for the participant across this+previous periods"""
        for i, player in enumerate(self.in_all_rounds()):
            if self.role == "Manager":
                for offer in Offer.filter(manager=player, period=self.round_number):
                    yield offer
            else:
                for offer in Offer.filter(employee=player, period=self.round_number):
                    yield offer

    @property
    def offer_history(self) -> List[Offer]:
        """Return a history of all (non-open) offers for the participant across this+previous periods"""
        offer_history = []

        for player in self.in_all_rounds():
            if self.role == "Manager":
                offer_history += Offer.filter(manager=player)
            else:
                offer_history += Offer.filter(employee=player)

        ## Remove open offers (only really matters for Employees)
        #offer_history = [offer for offer in offer_history if offer.accepted or offer.rejected]

        # Reverse the list of offers: most recent first
        return list(reversed(offer_history))

    @property
    def payoff_history(self) -> List[int]:
        """Return a history of payoffs for all periods."""
        payoff_history = []

        for player in self.in_all_rounds():
            payoff_history.append(player.payoff)

        return payoff_history


def offer_wage_max(player: Player):
    return player.session.config["max_wage"]

def offer_employee_choices(manager: Player):
    """Dynamically provide employee choices"""
    employee_ids = [employee.id_in_group for employee in manager.for_hire()]
    return employee_ids + [0] # It's always possible to reject all offers with 0

def player_matched_choices(employee: Player):
    """Dynamically provide offer choices"""
    open_offers = Offer.filter(employee=employee, accepted=False, rejected=False)
    manager_ids = [offer.manager.id_in_group for offer in open_offers]

    return manager_ids + [0] # It's always possible to reject all offers with 0


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value

class Group(BaseGroup):
    """Group object for simulation"""

    @property
    def managers(self) -> List[Player]:
        """Return all Manager players from the current group"""
        return [player for player in self.get_players() if player.role == "Manager"]

    @property
    def employees(self) -> List[Player]:
        """Return all Employee players from the current group"""
        return [player for player in self.get_players() if player.role == "Employee"]


# Extra models

class Offer(ExtraModel):
    """An offer from manager to employee"""
    period   = models.IntegerField()               # Period in which the offer was made
    step     = models.IntegerField()               # Hiring step in which the offer was made
    manager  = models.Link(Player)                 # Manager that made the offer
    employee = models.Link(Player)                 # Employee to which the offer was made
    group    = models.Link(Group)                  # Group that the Manager/Employee belonged to
    wage     = models.CurrencyField()              # Offered wage
    training = models.BooleanField()               # Whether training is included
    accepted = models.BooleanField(initial=False)  # True if Employee accepted (offer becomes contract)
    rejected = models.BooleanField(initial=False)  # True is Employee rejected (same Manager can't do another offer this Period)
    effort   = models.IntegerField(initial=0)      # Effort exerted by the Employee (after the work phase)
    revenue  = models.CurrencyField(initial=cu(0)) # Revenue generated by the Employee (after the work phase)

    @property
    def effort_cost(self):
        """Return cost of effort (negative) for selected effort"""
        if self.effort > 0:
            return -cu(self.manager.session.config["effort_costs"][self.effort - 1]) # pylint: disable=no-member
        else:
            return 0

    @property
    def manager_costs(self):
        """Return costs to the manager (negative) which is wage + training"""
        if self.training > 0:
            return -(self.wage + cu(self.manager.session.config["training_cost"])) # pylint: disable=no-member
        else:
            return -self.wage

    @property
    def employee_earnings(self) -> int:
        config = self.group.session.config
        return calculate_employee_payoff(config["employee_endowment"], int(self.wage),
                                         -config["effort_costs"][self.effort - 1])

    @property
    def manager_earnings(self) -> int:
        config = self.group.session.config
        effort = self.effort
        skill_multiplier = config["skill_multipliers"][self.employee.skill - 1]
        base_revenue = config["base_revenue"]
        initial_revenue = base_revenue * skill_multiplier * effort

        return calculate_manager_revenue_and_payoff(self.group, self.manager, initial_revenue, int(self.wage),
                                                    self.training)["payoff"]

# Pages

def stage_counter(player: Player, with_step: bool = False) -> str:
    """Formatted period + stage counter for display in titles"""
    return (f"(Period { player.subsession.round_number }/{ C.NUM_ROUNDS }"
            + (f" | Step { player.offer_step }/{ C.HIRING_STEPS })" if with_step else ")"))


class WaitForAllPlayers(WaitPage):
    """Wait page to synchronize everyone before a Period starts. Used to set skill levels appropriately."""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": "Waiting for all participants " + stage_counter(player),
            "body_text": "Please wait until all participants have entered this Period..."
        }

    # Use this Page to set skill from previous period + increase if necessary
    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.round_number > 1:
            for player in group.get_players():
                prev_player = player.in_round(group.round_number - 1)
                player.skill = prev_player.skill
                if prev_player.skill_increase:
                    player.skill = min(player.skill + 1, len(group.session.config["skill_multipliers"]))

class MakeOffer(Page):
    """Hiring phase page. Shown to Managers without an accepted offer who still can hire."""
    form_model = "player"
    form_fields = ["offer_employee", "offer_wage", "offer_training"]

    @staticmethod
    def vars_for_template(player):
        # List that holds data for building an employee table (both eligible and ineligible)
        employee_pool = [ {
            "employee": employee,
            "rejected": employee.rejected_from(player),
            "eligible": employee.choice_id(player) >= 0,
            "choice_id": employee.choice_id(player)
        } for employee in player.group.employees ]

        return {
            "employee_pool": employee_pool,
            "offers": player.offer_history,
            "eligible_offers": len([choice for choice in employee_pool if choice["eligible"]]),
            "future_periods": range(player.round_number, C.NUM_ROUNDS + 1)
        }

    # Shown only the player is a Manager,
    # without an accepted offer (= matched employee),
    # that didn't select to present no more offers
    # and still has eligible candidates
    @staticmethod
    def is_displayed(player: Player):
        return player.role == "Manager" and \
               player.player_matched == 0 and \
               not player.offer_none and \
               len(player.for_hire()) > 0

    @staticmethod
    def get_timeout_seconds(player: Player):
        """
        Otree page hook to decide how many seconds to wait until the page auto-submits.
        If player is an agent, it waits for timeout_seconds. Otherwise, it returns None.
        """
        if should_use_agent(player):
            timeout_seconds = 20
            return timeout_seconds  # Enough for LLM API calls to complete
        return None

    def make_offer_helper(player: Player):
        """
        Helper function for the agent to make the offers
        """
        game_state = build_make_offer_state(player, MakeOffer)
        offer = make_agent_offer(player, game_state)
        return offer
        

    @property
    def timeout_submission(self):
        """
        Auto-submit for agents on timeout (oTree uses timeout_submission).
        """
        player = self.player
        if not should_use_agent(player):
            return {}
        print(f"DEBUG timeout_submission MakeOffer for Manager {player.id_in_group}")
        return MakeOffer.make_offer_helper(player)

    @staticmethod
    def before_next_page(manager: Player, timeout_happened: bool):
        
        if manager.offer_employee > 0:
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
        else:
            manager.offer_none = True

class WaitForOffers(WaitPage):
    """Wait for offers page"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for offers { stage_counter(player, with_step=True) }",
            "body_text": "You are a Worker. Please wait until all employers have made their offers..."
        }

    # Shown to Employees without a contract
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
        return {
            "open_offers": open_offers,
            "num_offers": len(open_offers),
            "offers": player.offer_history,
            "future_periods": range(player.round_number, C.NUM_ROUNDS + 1)
        }

    # Shown to Employees without a contract, but with open offers in this step
    @staticmethod
    def is_displayed(player):
        open_offers = Offer.filter(employee=player, accepted=False, rejected=False)
        return player.role == "Employee" and player.player_matched == 0 and len(open_offers) > 0

    @staticmethod
    def get_timeout_seconds(player: Player):
        """
        Otree page hook to decide how many seconds to wait until the page auto-submits.
        If player is an agent, it waits for timeout_seconds. Otherwise, it returns None.
        """
        if should_use_agent(player):
            timeout_seconds = 20
            return timeout_seconds  # Enough for LLM API calls to complete
        return None

    def get_offer_helper(player: Player):
        """
        Helper function for the agent to get the offers
        """
        game_state = build_get_offers_state(player, GetOffers)
        offer = get_agent_offer(player, game_state)
        return offer


    @property
    def timeout_submission(self): 
        """
        Auto-submit for agents on timeout (oTree uses timeout_submission).
        """
        player = self.player
        if not should_use_agent(player):
            return {}
        return GetOffers.get_offer_helper(player)
    # Helper function for the agent to get the offers
    
    # Accept an offer (if any accepted), mark others rejected
    @staticmethod
    def before_next_page(employee: Player, timeout_happened: bool):
        if employee.player_matched > 0:
            manager = employee.group.get_player_by_id(employee.player_matched)
            manager.player_matched = employee.id_in_group

            offers = Offer.filter(manager=manager, employee=employee, accepted=False, rejected=False)
            assert len(offers) == 1
            accepted_offer = offers[0]

            accepted_offer.accepted = True
            employee.offer_wage = accepted_offer.wage
            employee.offer_training = accepted_offer.training
            if timeout_happened:
                print(f"Timeout for Worker {employee.id_in_group}, using smart default to accept manager {manager.id_in_group}'s offer (wage {accepted_offer.wage})")
        else:
            if timeout_happened:
                print(f"Timeout for Worker {employee.id_in_group}, no eligible offers to accept")

        open_offers = Offer.filter(employee=employee, accepted=False, rejected=False)
        for offer in open_offers:
            offer.rejected = True


class MatchSummary(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return 1

    @staticmethod
    def vars_for_template(player: Player):
        config = player.session.config

        if player.role == "Manager":
            contract = player.field_maybe_none("contract")

            if contract:
                # Match.
                body_text = "Once you are ready to proceed, click the button below."
                partner_title = contract.employee.label
                salary = contract.wage
                training = contract.training
            else:
                # No match.
                body_text = ("Your final choice was not to make an offer to any worker. For the following "
                              "work phase, you will only receive your initial endowment of "
                              f"{cu(config["manager_endowment"])}. You will now wait for others to finish "
                              "the work phase and then return to the labor market for the next period."
                              if player.offer_none else
                              "Your contract offer was not accepted. You will now return to the waiting page "
                              "and then to the labor market.")
                partner_title = None
                salary = None
                training = None
        else:
            contract = player.field_maybe_none("contract")

            if contract:
                # Match.
                body_text = "Once you are ready to advance to the work phase, click the button below."
                partner_title = player.contract.manager.label
                salary = player.contract.wage
                training = player.contract.training
            else:
                # No match.
                rejected_offers = Offer.filter(employee=player, rejected=True)
                body_text = ("You did not contract with an employer. "
                             "You will now return to the waiting page and then to the labor market."
                             if len(rejected_offers) != 0 else
                             "No employer made you an offer. You will now wait for others to finish the work phase "
                             "and then return to the labor market.")
                partner_title = None
                salary = None
                training = None

        return {
            "body_text": body_text,
            "partner_title": partner_title,
            "salary": salary,
            "training": "Y" if training else "N",
            "offers": player.offer_history,
            "future_periods": range(player.round_number, C.NUM_ROUNDS + 1)
        }

class WaitForAcceptance(WaitPage):
    """Wait for acceptance page; shown to Managers without a match or Employees without a valid offer."""
    @staticmethod
    def vars_for_template(player: Player):
        if player.role == "Manager":
            return {
                "title_text": f"Waiting for offer acceptance { stage_counter(player, with_step=True) }",
                "body_text": "You are an Employer. Please wait until all workers decide on their offers..."
            }
        else:
            offers_status = "You did not receive any offers at this hiring step."\
                if len(Offer.filter(employee=player)) == 0 else "You rejected all offers at this hiring step."
            return {
                "title_text": f"Waiting for offer acceptance { stage_counter(player, with_step=True) }",
                "body_text": f"You are a Worker. {offers_status} "
                             f"Please wait until all workers decide on their offers..."
            }

    # Shown to:
    # 1) Managers without a match (yet) that didn't choose "no offers",
    # 2) Employees without a match that didn't get offers (and didn't get shown GetOffers) or rejected all offers
    @staticmethod
    def is_displayed(player: Player):
        open_offers = Offer.filter(employee=player, accepted=False, rejected=False)
        return (player.role == "Manager" and player.player_matched == 0 and not player.offer_none) or \
            (player.role == "Employee" and player.player_matched == 0 and len(open_offers) == 0)

    # For everyone still looking, advance Hiring phase step
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.offer_step += 1


class ChooseEffort(Page):
    """Page where employees choose how much effort to apply"""
    form_model = "player"
    form_fields = ["work_effort"]

    # Shown to Employees with a match
    @staticmethod
    def is_displayed(player: Player):
        return player.role == "Employee" and player.player_matched > 0

    @staticmethod
    def get_timeout_seconds(player: Player):
        """
        Otree page hook to decide how many seconds to wait until the page auto-submits.
        If player is an agent, it waits for timeout_seconds. Otherwise, it returns None.
        """
        if should_use_agent(player):
            timeout_seconds = 20
            return timeout_seconds  # Enough for LLM API calls to complete
        return None
    
    def choose_effort_helper(player: Player):
        """
        Helper function for the agent to choose the effort
        """
        game_state = build_choose_effort_state(player, ChooseEffort)
        effort = choose_agent_effort(player, game_state)
        return effort

    @property
    def timeout_submission(self):
        if not should_use_agent(self.player):
            return {}
        return ChooseEffort.choose_effort_helper(self.player)

        

    @staticmethod
    def vars_for_template(employee: Player):
        config = employee.session.config
        base_revenue = config["base_revenue"]
        employee_endowment = config["employee_endowment"]
        contract = employee.contract
        manager = contract.manager
        skill_multiplier = config["skill_multipliers"][employee.skill - 1]

        initial_revenues = [cu(base_revenue * skill_multiplier * effort) for effort in range(1, 11)]
        revenue_and_payoff = [calculate_manager_revenue_and_payoff(manager.group, manager, cu(revenue),
                                                                        contract.wage,
                                                                        contract.training)
                             for revenue in initial_revenues]
        employer_payoff_values = [revenue_and_payoff_item["payoff"] for revenue_and_payoff_item in revenue_and_payoff]
        employee_payoff_values = [calculate_employee_payoff(employee_endowment, contract.wage, -effort_cost)
                                  for effort_cost in config["effort_costs"]]

        return {
            "contract": contract,
            "offers": employee.offer_history,
            "effort_costs": config["effort_costs"],
            "employee_payoff_values": employee_payoff_values,
            "employer_payoff_values": employer_payoff_values,
            "future_periods": range(employee.round_number, C.NUM_ROUNDS + 1)
        }

    @staticmethod
    def js_vars(player):
        return {
            "manager_id": player.contract.manager.id_in_group
        }

    @staticmethod
    def before_next_page(employee: Player, timeout_happened: bool):
        # If timeout happened and no effort was chosen, try LLM first
        if timeout_happened and (employee.work_effort is None or employee.work_effort == 0):
            employee.work_effort = 5
            print(f"Timeout for Worker {employee.id_in_group}, using default effort level 5")
        
        # Record effort spent in the Offer table
        employee.contract.effort = employee.work_effort

class WaitForEffort(WaitPage):
    """Wait page until everyone finishes Work phase"""
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "title_text": f"Waiting for the work phase { stage_counter(player) }",
            "body_text": "Waiting for everyone to finish the work phase..."
        }

    # Main place where payoffs are calculated
    @staticmethod
    def after_all_players_arrive(group: Group):
        """Calculate all payoffs"""
        config = group.session.config

        for player in group.get_players():
            contract = player.field_maybe_none("contract")

            if player.role == "Employee":
                endowment = config["employee_endowment"]
                endowment_cu = cu(endowment)

                if contract:
                    print(f"Payoff for Worker {player.id_in_group}: {endowment_cu} + {contract.wage} - {-contract.effort_cost}")
                    player.payoff = cu(calculate_employee_payoff(endowment, contract.wage, contract.effort_cost))
                    if contract.training:
                        player.skill_increase = True
                else:
                    print(f"Payoff for Worker {player.id_in_group}: {endowment_cu}")
                    player.payoff = endowment_cu
            else:
                endowment_cu = cu(config["manager_endowment"])

                if contract:
                    effort = contract.employee.work_effort
                    skill_multiplier = config["skill_multipliers"][contract.employee.skill - 1]
                    base_revenue = config["base_revenue"]

                    initial_revenue = cu(base_revenue * skill_multiplier * effort)
                    has_training = contract.training
                    wage = contract.wage
                    revenue_and_payoff = calculate_manager_revenue_and_payoff(group, player, initial_revenue, wage,
                                                                      has_training)

                    print(revenue_and_payoff["message"])
                    contract.revenue = revenue_and_payoff["revenue"]
                    player.payoff = revenue_and_payoff["payoff"]
                else:
                    print(f"Payoff for Manager {player.id_in_group}: {endowment_cu}")
                    player.payoff = endowment_cu

            player.payoff_calculated = True

        # Print comprehensive round summary
        _print_round_summary(group)

class PeriodResults(Page):
    """Period outcomes display"""

    @staticmethod
    def get_timeout_seconds(player: Player):
        """
        Otree page hook to decide how many seconds to wait until the page auto-submits.
        If player is an agent, it waits for timeout_seconds. Otherwise, it returns None.
        """
        # Auto-advance agent players quickly (no form to submit, just informational)
        if should_use_agent(player):
            timeout_seconds = 1
            return timeout_seconds
        """
        Otree page hook to decide how many seconds to wait until the page auto-submits.
        If player is an agent, it waits for timeout_seconds. Otherwise, it returns None.
        """
        # Auto-advance agent players quickly (no form to submit, just informational)
        if should_use_agent(player):
            timeout_seconds = 1
            return timeout_seconds
        return None

    # A lot of payoff is calculated again here for display
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        session = group.session
        config = session.config
        manager_endowment = config["manager_endowment"]
        employee_endowment = config["employee_endowment"]
        skill_multipliers = config["skill_multipliers"]
        training_productivity_multiplier = config["training_productivity_multiplier"]

        if player.field_maybe_none("contract"):
            contract = player.contract
            skill = contract.employee.skill
            new_skill = min(skill + 1, len(skill_multipliers)) if contract.employee.skill_increase else skill
            skill_multiplier = skill_multipliers[skill - 1]
            new_skill_multiplier = skill_multipliers[new_skill - 1]
            base_revenue = player.session.config["base_revenue"]
            revenue = cu(base_revenue * skill_multiplier * contract.employee.work_effort)
            wage = contract.wage if contract else 0
            has_training = contract.training
            effort_cost = player.session.config["effort_costs"][contract.employee.work_effort - 1]
        else:
            skill = 0 if player.role == "Manager" else player.skill
            new_skill = skill
            skill_multiplier = 0 if player.role == "Manager" else skill_multipliers[skill - 1]
            new_skill_multiplier = skill_multiplier
            revenue = cu(0)
            wage = 0
            has_training = False
            effort_cost = 0

        productivity_reduction = round(revenue * training_productivity_multiplier) if has_training else 0
        direct_training_cost = config["training_cost"] if has_training else 0
        revenue_and_payoff = calculate_manager_revenue_and_payoff(group, player, revenue, wage, has_training)

        return {
            "offers": player.offer_history,
            "skill_multiplier": skill_multiplier,
            "new_skill_multiplier": new_skill_multiplier,
            "skill": skill,
            "new_skill": new_skill,
            "revenue": revenue,
            "negative_productivity_reduction": -productivity_reduction,
            "effort_cost": effort_cost,
            "negative_effort_cost": -effort_cost,
            "negative_direct_training_cost": -direct_training_cost,
            "negative_overall_training_cost": -direct_training_cost - productivity_reduction,
            "negative_wage": -wage,
            "revenue_and_payoff": revenue_and_payoff,
            "has_training": has_training,
            "manager_endowment": manager_endowment,
            "employee_endowment": employee_endowment,
            "future_periods": range(player.round_number + 1, C.NUM_ROUNDS + 1),
            "agent_reasoning_log": player.participant.vars.get("agent_reasoning_log", []),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print(f"Timeout for Player {player.id_in_group}.")

        if player.round_number == C.NUM_ROUNDS:
            player.participant.vars["labor_dump"] = {
                "payoff_history": player.payoff_history,
            }


# ============================================================================
# GAME SUMMARY PRINTER
# ============================================================================

def _print_round_summary(group: Group):
    """Print a comprehensive summary of the round's decisions and outcomes and save to file"""
    
    try:
        # Build summary text
        summary_lines = []
        summary_lines.append("\n" + "="*80)
        summary_lines.append(f"ROUND {group.get_players()[0].round_number} SUMMARY")
        summary_lines.append("="*80)
        
        # HIRING PHASE SUMMARY
        summary_lines.append("\n--- HIRING PHASE ---")
        all_offers = Offer.filter(group=group)
        
        if all_offers:
            summary_lines.append("\nOffers Made:")
            offers_by_manager = defaultdict(list)
            for offer in all_offers:
                offers_by_manager[offer.manager.id_in_group].append(offer)
            
            for manager_id in sorted(offers_by_manager.keys()):
                offers = offers_by_manager[manager_id]
                for offer in offers:
                    status = "✓ ACCEPTED" if offer.accepted else ("✗ REJECTED" if offer.rejected else "PENDING")
                    training_str = " + TRAINING" if offer.training else ""
                    summary_lines.append(f"  Manager {manager_id} → Worker {offer.employee.id_in_group}: "
                          f"${offer.wage}{training_str} [{status}]")
        else:
            summary_lines.append("No offers made this round")
        
        # CONTRACTS
        summary_lines.append("\nContracts Formed:")
        contracts = []
        for player in group.get_players():
            if player.role == "Manager":
                contract = player.field_maybe_none("contract")
                if contract:
                    contracts.append((player.id_in_group, contract))
        
        if contracts:
            for manager_id, contract in contracts:
                training_str = " + TRAINING" if contract.training else ""
                summary_lines.append(f"  Manager {manager_id} ↔ Worker {contract.employee.id_in_group}: "
                      f"${contract.wage}{training_str}")
        else:
            summary_lines.append("No contracts formed this round")
        
        # EFFORT PHASE
        summary_lines.append("\nEffort Choices:")
        effort_decisions = []
        for player in group.get_players():
            if player.role == "Employee" and player.field_maybe_none("contract"):
                effort = player.work_effort or 0
                effort_decisions.append((player.id_in_group, effort))
        
        if effort_decisions:
            for worker_id, effort in sorted(effort_decisions):
                summary_lines.append(f"  Worker {worker_id}: Effort {effort}/10")
        else:
            summary_lines.append("No effort choices (no active contracts)")
        
        # PAYOFFS
        summary_lines.append("\nPayoffs This Round:")
        for player in group.get_players():
            if player.payoff_calculated:
                role_label = "Manager" if player.role == "Manager" else "Worker"
                payoff_value = player.payoff if hasattr(player, 'payoff') else 0
                summary_lines.append(f"  {role_label} {player.id_in_group}: {payoff_value} points")
        
        summary_lines.append("="*80 + "\n")
        
        # Print to console
        summary_text = "\n".join(summary_lines)
        print(summary_text)
        
        # Save to file
        exports_dir = Path(__file__).parent.parent / "_exports"
        exports_dir.mkdir(exist_ok=True)
        
        session_id = group.session.code
        summary_file = exports_dir / f"game_summary_{session_id}.txt"
        
        # Add header if this is a new file
        if not summary_file.exists():
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(f"GAME SUMMARY - Session {session_id}\n")
                f.write(f"Session: {session_id}\n")
                f.write("="*80 + "\n\n")
        
        # Append the round summary
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(summary_text)
        
        print(f"[Saved to {summary_file}]")
        
    except Exception as e:
        print(f"[ERROR in _print_round_summary: {e}]")


# Repeat for NUM_ROUNDS periods (rounds/subsessions)
# * WaitForAllPlayers to set skill levels based on previous period
# Hiring Phase:
#   Repeat HIRING_STEPS times the Hiring Phase step:
#   * MakeOffer is shown to Managers who can still make offers
#   * WaitForOffers is shown to Employees who are not matched until all offers are made
#   * GetOffers is shown to Employees with open offers, to accept or reject
#   * WaitForAcceptance is show to all without a match
#   (Whoever has a match falls through to the Work phase)
# Work Phase:
# * MatchSummary is shown to all players to inform them if they have made a contract.
# * ChooseEffort is shown to Employees with contracts to select effort
# * WaitForEffort is shown to everyone until all effort is selected
# Results Phase:
# * PeriodResults is shown to everyone to summarize their payoffs

page_sequence = [WaitForAllPlayers] + [MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * C.HIRING_STEPS + [MatchSummary, ChooseEffort, WaitForEffort, PeriodResults]
