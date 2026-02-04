from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Optional

from agent.prompts import (
    system_prompt_choose_effort,
    system_prompt_make_offer,
    system_prompt_get_offers,
)


DEFAULT_AGENT_SETTINGS: Dict[str, Any] = {
    "model_name": "gpt-4.1",
    "temperature": 0.2,
    "system_prompts": {
        "make_offer": system_prompt_make_offer,
        "get_offers": system_prompt_get_offers,
        "choose_effort": system_prompt_choose_effort,
    },
    "min_wage": 1,
}


def _normalize_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def get_agent_settings(player: Optional[Any] = None) -> Dict[str, Any]:
    settings = deepcopy(DEFAULT_AGENT_SETTINGS)
    if player is None:
        return settings
    session_cfg = player.session.config if hasattr(player, "session") else {}
    overrides = session_cfg.get("agent_settings", {})
    if isinstance(overrides, dict):
        settings.update({k: v for k, v in overrides.items() if k != "system_prompts"})
        prompt_overrides = overrides.get("system_prompts")
        if isinstance(prompt_overrides, dict):
            settings["system_prompts"].update(prompt_overrides)
    model_name = session_cfg.get("agent_model_name")
    temperature = session_cfg.get("agent_temperature")
    if model_name:
        settings["model_name"] = model_name
    if temperature is not None:
        settings["temperature"] = temperature
    return settings


def should_use_agent(player: Any) -> bool:
    participant = getattr(player, "participant", None)
    if participant is not None:
        override = participant.vars.get("use_agent")
        normalized = _normalize_bool(override)
        if normalized is not None:
            return normalized
    session_cfg = player.session.config if hasattr(player, "session") else {}
    agent_player_ids = session_cfg.get("agent_player_ids", [])
    if isinstance(agent_player_ids, (list, tuple, set)):
        return player.id_in_group in agent_player_ids
    return False
