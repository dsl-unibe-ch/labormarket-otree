"""
Defines the agent policies for steps in the labor market game.
"""
from typing import TYPE_CHECKING
from pathlib import Path

from agent.config import get_agent_settings
from agent.agent import Agent

if TYPE_CHECKING:
    from labor_market import Player


def append_agent_reasoning(player: "Player", page_name: str, decision: dict | None):
    participant = player.participant
    log = participant.vars.get("agent_reasoning_log", [])
    if not isinstance(log, list):
        log = []
    log.append(
        {
            "round": player.round_number,
            "step": player.offer_step,
            "page": page_name,
            "decision": decision or {},
            "reasoning": (decision or {}).get("reasoning"),
        }
    )
    participant.vars["agent_reasoning_log"] = log
    session_id = player.session.code
    
    # Get exports_dir from config with fallback
    exports_dir = player.session.config.get("exports_dir")
    if exports_dir is None:
        # Fallback to default _exports directory
        exports_dir = Path(__file__).parent.parent / "_exports"
    elif not isinstance(exports_dir, Path):
        exports_dir = Path(exports_dir)
    
    exports_dir.mkdir(exist_ok=True)
    reasoning_file = exports_dir / f"reasoning_{session_id}.txt"
    if not reasoning_file.exists():
        with open(reasoning_file, "w", encoding="utf-8") as f:
            f.write(f"REASONING - Session {session_id}\n")
            f.write(f"Session: {session_id}\n")
            f.write("="*80 + "\n\n")
    with open(reasoning_file, "a", encoding="utf-8") as f:
        f.write(f"Player {player.id_in_group} ({player.role}) - Period {player.round_number} - Step {player.offer_step} - {page_name}\n")
        
        # Write the full decision data (excluding reasoning which is written separately)
        decision_data = {k: v for k, v in (decision or {}).items() if k != 'reasoning'}
        if decision_data:
            f.write(f"Decision: {decision_data}\n")
        else:
            f.write(f"Decision: N/A\n")
        
        reasoning = (decision or {}).get('reasoning', 'N/A')
        f.write(f"Reasoning: {reasoning}\n")
        f.write("="*80 + "\n\n")


def normalize_offer_employee(value, eligible_ids):
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


def normalize_wage(value, default=100, min_wage=1, max_wage=None):
    try:
        wage = int(value)
    except (TypeError, ValueError):
        print(f"DEBUG wage = {value} is not a valid integer, using default {default}")
        wage = default
    wage = max(min_wage, wage)
    if max_wage is not None:
        wage = min(max_wage, wage)
    print(f"DEBUG normalized wage = {wage}")
    return wage

def normalize_training(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return default

def normalize_player_matched(value, eligible_manager_ids):
    try:
        manager_id = int(value)
    except (TypeError, ValueError):
        manager_id = None
    if manager_id in eligible_manager_ids:
        return manager_id
    return 0

def normalize_effort(value, default=5):
    try:
        effort = int(value)
    except (TypeError, ValueError):
        effort = default
    return max(1, min(10, effort))


def make_agent_offer(player: "Player", game_state: dict) -> dict:
    """
    Defines the agent policy for the make offer step.
    """
    eligible_employee_ids = game_state["eligible_employee_ids"]
    print(f"DEBUG Manager {player.id_in_group}: eligible_employee_ids = {eligible_employee_ids}")
    settings = get_agent_settings(player)
    offer_wage = settings.get("min_wage", 1)
    offer_training = False
    agent = Agent(
        model_name=settings["model_name"],
        temperature=settings["temperature"],
        system_prompt=settings["system_prompts"]["make_offer"],
    )
    decision = agent.make_offer(
        participant_id=player.id_in_group,
        game_state=game_state,
    )
    print(f"Agent decision (MakeOffer) for Manager {player.id_in_group}: {decision}")
    if isinstance(decision, dict):
        print(f"Agent reasoning (MakeOffer) for Manager {player.id_in_group}: {decision.get('reasoning')}")
    append_agent_reasoning(player, "MakeOffer", decision)
    offer_employee = normalize_offer_employee(
        decision.get("offer_employee"),
        eligible_employee_ids,
    )
    offer_wage = normalize_wage(
        decision.get("offer_wage"),
        default=offer_wage,
        min_wage=settings.get("min_wage", 1),
        max_wage=game_state["max_wage"],
    )
    offer_training = normalize_training(
        decision.get("offer_training"),
        default=offer_training,
    )
    if offer_employee == 0:
        print(
            f"Agent chose no offer for Manager {player.id_in_group} with eligible IDs: "
            f"{eligible_employee_ids}"
        )
        offer_wage = settings.get("min_wage")
        offer_training = False

    return {
        "offer_employee": offer_employee,
        "offer_wage": offer_wage,
        "offer_training": offer_training
    }

def get_agent_offer(player: "Player", game_state: dict) -> dict:
    """
    Defines the agent policy for the get offers step.
    """
    settings = get_agent_settings(player)
    agent = Agent(
        model_name=settings["model_name"],
        temperature=settings["temperature"],
        system_prompt=settings["system_prompts"]["get_offers"],
    )
    decision = agent.respond_to_offer(
        participant_id=player.id_in_group,
        game_state=game_state,
    )
    print(f"Agent decision (GetOffers) for Worker {player.id_in_group}: {decision}")
    if isinstance(decision, dict):
        print(f"Agent reasoning (GetOffers) for Worker {player.id_in_group}: {decision.get('reasoning')}")
    append_agent_reasoning(player, "GetOffers", decision)
    eligible_manager_ids = game_state["eligible_manager_ids"]
    manager_id = normalize_player_matched(
        decision.get("player_matched"),
        eligible_manager_ids,
    )
    return {
        "player_matched": manager_id,
    }


def choose_agent_effort(player: "Player", game_state: dict) -> dict:
    """
    Defines the agent policy for the choose effort step.
    """
    settings = get_agent_settings(player)
    agent = Agent(
        model_name=settings["model_name"],
        temperature=settings["temperature"],
        system_prompt=settings["system_prompts"]["choose_effort"],
    )
    decision = agent.choose_effort(
        participant_id=player.id_in_group,
        game_state=game_state,
    )
    print(f"Agent decision (ChooseEffort) for Worker {player.id_in_group}: {decision}")
    if isinstance(decision, dict):
        print(f"Agent reasoning (ChooseEffort) for Worker {player.id_in_group}: {decision.get('reasoning')}")
    append_agent_reasoning(player, "ChooseEffort", decision)
    work_effort = normalize_effort(decision.get("work_effort"), default=5)
    return {"work_effort": work_effort}
