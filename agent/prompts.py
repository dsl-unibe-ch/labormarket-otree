from pathlib import Path
import re


_TEMPLATE_DIR = Path(__file__).parent.parent / "labor_market"


def _extract_template_instructions(template_name: str) -> list[str]:
    path = _TEMPLATE_DIR / template_name
    try:
        html = path.read_text(encoding="utf-8")
    except OSError:
        return []
    blocks = []
    for tag in ("h3", "p"):
        blocks.extend(re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", html, flags=re.DOTALL))
    cleaned = []
    for block in blocks:
        block = re.sub(r"{[{%].*?[}%]}", " ", block, flags=re.DOTALL)
        block = re.sub(r"<[^>]+>", " ", block)
        block = " ".join(block.split())
        if block:
            cleaned.append(block)
    return cleaned


def _build_system_prompt(base: str, template_name: str, response_format: str) -> str:
    instructions = _extract_template_instructions(template_name)
    if instructions:
        instruction_text = "Page instructions:\n- " + "\n- ".join(instructions)
        return f"{base}\n{instruction_text}\n{response_format}"
    return f"{base}\n{response_format}"


def build_system_prompt_choose_effort() -> str:
    base = (
        "You are an Employee in a labor market experiment. "
        "Choose an effort level from 1 to 10 that maximizes your payoff, "
        "considering wage, training, and effort costs."
    )
    response_format = "Return only JSON with keys work_effort and reasoning."
    return _build_system_prompt(base, "ChooseEffort.html", response_format)


def build_system_prompt_make_offer() -> str:
    base = (
        "You are a Manager in a labor market experiment. "
        "Make an offer to an Employee that maximizes your payoff, "
        "considering wage, training, and effort costs. "
        "You may choose no offer by setting offer_employee to 0."
    )
    response_format = (
        "Return only JSON with keys offer_employee, offer_wage, offer_training, and reasoning."
    )
    return _build_system_prompt(base, "MakeOffer.html", response_format)


def build_system_prompt_get_offers() -> str:
    base = (
        "You are an Employee in a labor market experiment. "
        "Decide whether to accept one offer or reject all."
    )
    response_format = "Return only JSON with keys player_matched and reasoning."
    return _build_system_prompt(base, "GetOffers.html", response_format)


system_prompt_choose_effort = build_system_prompt_choose_effort()
system_prompt_make_offer = build_system_prompt_make_offer()
system_prompt_get_offers = build_system_prompt_get_offers()