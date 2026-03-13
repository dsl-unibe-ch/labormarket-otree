"""
Prepares the game state for the agent to make the offers
"""

from agent.config import get_agent_settings


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value

def build_make_offer_state(player, MakeOfferPage) -> dict:
    """
    Prepares the game state for the agent to make the offers
    """
    settings = get_agent_settings(player)
    template_vars = MakeOfferPage.vars_for_template(player)
    employee_pool = template_vars["employee_pool"]
    eligible_employee_ids = [
        item["employee"].id_in_group for item in employee_pool if item["eligible"]
    ]
    max_wage = _to_int(player.session.config.get("max_wage"))
    game_state = {
        "round_number": player.round_number,
        "current_hiring_step": player.offer_step,
        "manager_id": player.id_in_group,
        "eligible_employee_ids": eligible_employee_ids,
        "allow_no_offer": True,
        "min_wage": settings.get("min_wage", 1),
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
        "offers": [
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
        ],
        "future_periods": list(template_vars["future_periods"]),
    }
    return game_state


def build_get_offers_state(player, GetOffersPage) -> dict:
    """
    Prepares the game state for the agent to get the offers    
    """
    template_vars = GetOffersPage.vars_for_template(player)
    open_offers = template_vars["open_offers"]
    eligible_manager_ids = [offer.manager.id_in_group for offer in open_offers] + [0]
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
        "round_number": player.round_number,
        "employee_id": player.id_in_group,
        "skill": player.skill,
        "offers": offers,
        "eligible_manager_ids": eligible_manager_ids,
        "future_periods": list(template_vars["future_periods"]),
    }
    return game_state

def build_choose_effort_state(player, ChooseEffortPage) -> dict:
    """
    Prepares the game state for the agent to choose the effort
    """
    template_vars = ChooseEffortPage.vars_for_template(player)
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
        "round_number": player.round_number,
        "employee_id": player.id_in_group,
        "skill": player.skill,
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
    return game_state

