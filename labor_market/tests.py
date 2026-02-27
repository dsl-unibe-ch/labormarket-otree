"""
Bot tests for labor_market app
"""

from otree.api import Bot, Submission
from agent.agent import Agent
from agent.config import get_agent_settings
from . import (
    MakeOffer, GetOffers,
    MatchSummary, ChooseEffort, PeriodResults
)


def _normalize_effort(value, default=5):
    try:
        effort = int(value)
    except (TypeError, ValueError):
        effort = default
    return max(1, min(10, effort))

def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value

def _normalize_wage(value, default=100, min_wage=1, max_wage=None):
    try:
        wage = int(value)
    except (TypeError, ValueError):
        wage = default
    wage = max(min_wage, wage)
    if max_wage is not None:
        wage = min(max_wage, wage)
    return wage

def _normalize_training(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return default

def _normalize_offer_employee(value, eligible_ids):
    try:
        employee_id = int(value)
    except (TypeError, ValueError):
        employee_id = None
    if employee_id == 0:
        return 0
    if employee_id in eligible_ids:
        return employee_id
    if eligible_ids:
        return eligible_ids[0]
    return 0

def _normalize_player_matched(value, eligible_manager_ids):
    try:
        manager_id = int(value)
    except (TypeError, ValueError):
        manager_id = None
    if manager_id in eligible_manager_ids:
        return manager_id
    return 0


class PlayerBot(Bot):
    """Bot that plays through the labor market simulation"""
    """
    This bot simulates the labor market hiring and work phase where:
        - Managers make contract offers to employees (up to 6 attempts)
        - Employees accept or reject offers
        - Then matched pairs complete the work phase 
    """
    
    def play_round(self):
        """Play through one round of the labor market"""
        
        # The page sequence repeats: [MakeOffer, WaitForOffers, GetOffers, WaitForAcceptance] * 6 times
        # Then: MatchSummary, ChooseEffort, WaitForEffort, PeriodResults
        # (WaitPages are handled automatically, don't yield them)
        # Only yield pages that will actually be displayed to this player
        
        for step in range(6):  # 6 hiring steps
            # Managers make offers only when MakeOffer is displayed
            if MakeOffer.is_displayed(self.player):

                # Get list of available employees to hire
                # Returns list of employees who: are not matched, haven't rejected this manager's previous offers
                available = self.player.for_hire()

                if available:

                    # Make an offer to first available employee
                    # Takes first employee from available list: available[0]
                    # Gets their ID: id_in_group (e.g., 7, 8, 9...)
                    # Submits offer with employee ID, wage, and training choice
                    template_vars = MakeOffer.vars_for_template(self.player)
                    employee_pool = template_vars["employee_pool"]
                    eligible_pool = [item for item in employee_pool if item["eligible"]]
                    eligible_ids = [item["employee"].id_in_group for item in eligible_pool]
                    offers = [
                        {
                            "period": offer.period,
                            "step": offer.step,
                            "employee_id": offer.employee.id_in_group,
                            "wage": _to_int(offer.wage),
                            "training": offer.training,
                            "accepted": offer.accepted,
                            "rejected": offer.rejected,
                        }
                        for offer in template_vars["offers"]
                    ]
                    max_wage = _to_int(self.player.session.config.get("max_wage"))
                    game_state = {
                        "round_number": self.player.round_number,
                        "manager_id": self.player.id_in_group,
                        "eligible_employee_ids": eligible_ids,
                        "allow_no_offer": True,
                        "min_wage": 1,
                        "max_wage": max_wage,
                        "employee_pool": [
                            {
                                "employee_id": item["employee"].id_in_group,
                                "skill": item["employee"].skill,
                                "rejected": item["rejected"],
                                "eligible": item["eligible"],
                                "choice_id": item["choice_id"],
                            }
                            for item in employee_pool
                        ],
                        "offers": offers,
                        "future_periods": list(template_vars["future_periods"]),
                    }
                    employee_id = eligible_ids[0]
                    offer_wage = 100
                    offer_training = False
                    try:
                        agent_settings = get_agent_settings(self.player)
                        agent = Agent(
                            model_name=agent_settings["model_name"],
                            temperature=agent_settings["temperature"],
                            system_prompt=agent_settings["system_prompts"]["make_offer"],
                        )
                        decision = agent.make_offer(
                            participant_id=self.player.id_in_group,
                            game_state=game_state,
                        )
                        employee_id = _normalize_offer_employee(
                            decision.get("offer_employee"),
                            eligible_ids,
                        )
                        offer_wage = _normalize_wage(
                            decision.get("offer_wage"),
                            default=100,
                            min_wage=1,
                            max_wage=max_wage,
                        )
                        offer_training = _normalize_training(
                            decision.get("offer_training"),
                            default=False,
                        )
                    except Exception as exc:
                        print(f"Agent decision failed, using default offer: {exc}")
                    if employee_id == 0:
                        offer_wage = _normalize_wage(
                            offer_wage,
                            default=1,
                            min_wage=1,
                            max_wage=max_wage,
                        )
                        offer_training = False

                    yield Submission(
                        MakeOffer,
                        {
                            'offer_employee': employee_id,
                            'offer_wage': offer_wage,  # Player Decision
                            'offer_training': offer_training  # Player Decision
                        },
                        check_html=False
                    )
                else:
                    # No eligible candidates; page should not be displayed
                    pass
            
            # Employees accept offers if they have any (only shown if unmatched and has open offers)
            # Only employees who are not matched respond to offers
            # Once matched, skip this block
            if self.player.role == "Employee" and self.player.player_matched == 0:

                # Check for open offers (not accepted or rejected)
                # self.player.offer_history: List of all offers received
                # Filter for offers that are not accepted and not rejected --> open offers
                open_offers = [o for o in self.player.offer_history 
                              if not o.accepted and not o.rejected]
                
                # accepts first open offer
                # Takes first open offer: open_offers[0]
                # Gets the manager's ID who made that offer: manager.id_in_group
                # Submits acceptance by setting player_matched to that manager's ID
                if open_offers:
                    # for this employee use the Getoffers class to get vars_for_template to understand the open offer details
                    template_vars = GetOffers.vars_for_template(self.player)
                    eligible_manager_ids = [
                        offer.manager.id_in_group for offer in open_offers
                    ] + [0]
                    offers = [
                        {
                            "period": offer.period,
                            "step": offer.step,
                            "manager_id": offer.manager.id_in_group,
                            "wage": _to_int(offer.wage),
                            "training": offer.training,
                        }
                        for offer in template_vars["offers"]
                    ]
                    game_state = {
                        "round_number": self.player.round_number,
                        "employee_id": self.player.id_in_group,
                        "skill": self.player.skill,
                        "offers": offers,
                        "eligible_manager_ids": eligible_manager_ids,
                        "future_periods": list(template_vars["future_periods"]),
                    }
                    manager_id = open_offers[0].manager.id_in_group
                    try:
                        agent_settings = get_agent_settings(self.player)
                        agent = Agent(
                            model_name=agent_settings["model_name"],
                            temperature=agent_settings["temperature"],
                            system_prompt=agent_settings["system_prompts"]["get_offers"],
                        )
                        decision = agent.respond_to_offer(
                            participant_id=self.player.id_in_group,
                            game_state=game_state,
                        )
                        manager_id = _normalize_player_matched(
                            decision.get("player_matched"),
                            eligible_manager_ids,
                        )
                    except Exception as exc:
                        print(f"Agent decision failed, using default acceptance: {exc}")
                    yield Submission(
                        GetOffers,
                        {'player_matched': manager_id},
                        check_html=False
                    )
        
        # After hiring phase, view match summary (no form submission)
        # Shows who matched with whom
        # Everyone sees this (matched or not)
        # Just displays results
        yield MatchSummary
        
        # Work Phase
        # Choose effort - only shown to EMPLOYEES who are matched
        # Managers don't see this page
        if self.player.role == "Employee" and self.player.player_matched > 0:
            # Gather the vars_for_template from ChooseEffort as variables based on which the work_effort is determined by the LLM
            template_vars = ChooseEffort.vars_for_template(self.player)
            contract = template_vars["contract"]
            offers = [
                {
                    "period": offer.period,
                    "step": offer.step,
                    "manager_id": offer.manager.id_in_group,
                    "wage": _to_int(offer.wage),
                    "training": offer.training,
                    "accepted": offer.accepted,
                    "rejected": offer.rejected,
                }
                for offer in template_vars["offers"]
            ]
            game_state = {
                "round_number": self.player.round_number,
                "employee_id": self.player.id_in_group,
                "skill": self.player.skill,
                "contract": {
                    "manager_id": contract.manager.id_in_group,
                    "wage": _to_int(contract.wage),
                    "training": contract.training,
                },
                "offers": offers,
                "effort_costs": [_to_int(cost) for cost in template_vars["effort_costs"]],
                "employee_payoff_values": [
                    _to_int(value) for value in template_vars["employee_payoff_values"]
                ],
                "employer_payoff_values": [
                    _to_int(value) for value in template_vars["employer_payoff_values"]
                ],
            }
           
            work_effort = 5
            try:
                agent_settings = get_agent_settings(self.player)
                agent = Agent(
                    model_name=agent_settings["model_name"],
                    temperature=agent_settings["temperature"],
                    system_prompt=agent_settings["system_prompts"]["choose_effort"],
                )
                decision = agent.choose_effort(
                    participant_id=self.player.id_in_group,
                    game_state=game_state,
                )
                work_effort = _normalize_effort(decision.get("work_effort"), default=5)
            except Exception as exc:
                print(f"Agent decision failed, using default effort: {exc}")

            yield Submission(
                ChooseEffort,
                {'work_effort': work_effort}, # Player Decision
                check_html=False
            )
        
        # View period results (only shown at end)
        # Shows earnings for the period
        # Everyone sees this
        # No form to submit
        yield PeriodResults


# Full Round Structure
# HIRING PHASE (repeats up to 6 times):
#   → MakeOffer (Managers only, if unmatched)
#   → WaitForOffers (automatic wait page)
#   → GetOffers (Employees only, if have offers)
#   → WaitForAcceptance (automatic wait page)

# WORK PHASE:
#   → MatchSummary (everyone sees this)
#   → ChooseEffort (Employees only, if matched)
#   → WaitForEffort (automatic wait page)
#   → PeriodResults (everyone sees this)


# Key Concept: Conditional Page Display
# Important: Not all players see all pages!
# Pages are shown based on conditions:

# - MakeOffer: Only if you're a Manager AND unmatched
# - GetOffers: Only if you're an Employee AND have pending offers
# - ChooseEffort: Only if you're an Employee AND matched

# The bot must only yield pages that will actually be shown to that player!

# ---------------------------------------------------------------------------

# Round 1:

# - All 6 managers make offers → All employees have offers
# - All employees accept → All matched
# - player_matched > 0 for everyone

# Round 2-6:

# - Managers check: if self.player.player_matched == 0 → False (already matched)
# - Employees check: if self.player.player_matched == 0 → False (already matched)
# - Nobody yields pages → Loop continues but pages don't display
# - Bot moves on to next phase

# If someone doesn't match:

# - Their player_matched stays 0
# - They keep trying in subsequent rounds
# - Loop gives them 6 chances total

# -----------------------------------------------------------------------------

# Visual Flow Example

# Manager Bot (Gets Matched Round 1):
# Round 1:
#   → MakeOffer (submit offer to Employee 7)
#   → [Wait automatically]
#   → [Employee accepts]
#   → player_matched = 7

# Round 2-6:
#   → Check: player_matched == 0? NO (it's 7)
#   → Don't yield MakeOffer
#   → Skip to work phase

# Work Phase:
#   → MatchSummary (view results)
#   → [Skip ChooseEffort - not an employee]
#   → PeriodResults (view earnings)



# Employee Bot (Gets Offer Round 1):
# Round 1:
#   → [Manager makes offer]
#   → GetOffers displays (has pending offer)
#   → Accept Manager 2
#   → player_matched = 2

# Round 2-6:
#   → Check: player_matched == 0? NO (it's 2)
#   → Don't yield GetOffers
#   → Skip to work phase

# Work Phase:
#   → MatchSummary (view results)
#   → ChooseEffort (submit effort=5)
#   → PeriodResults (view earnings)



# Unmatched Employee Bot:
# Round 1:
#   → No offers received
#   → Don't yield GetOffers

# Round 2:
#   → Gets offer from Manager 4
#   → GetOffers displays
#   → Accept Manager 4
#   → player_matched = 4

# Round 3-6:
#   → Matched, skip

# Work Phase:
#   → MatchSummary
#   → ChooseEffort (effort=5)
#   → PeriodResults
