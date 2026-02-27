# Labor Market oTree Experiment

An oTree experiment for studying decision-making in organizational labor market settings.

## High Level Description of the Steps

1. WaitForAllPlayers (sync at start of period)
2. Hiring phase repeats C.HIRING_STEPS times:
    1. MakeOffer (Managers only, if eligible)
    2. WaitForOffers (Employees wait for offers)
    3. GetOffers (Employees review/accept/reject offers)
3. WaitForAcceptance (everyone without a match waits)
4. MatchSummary (shows matches)
5. ChooseEffort (Employees with a contract choose effort)
6. WaitForEffort (wait for all effort choices)
7. PeriodResults (earnings summary)

## Setup

### 1. Initial Setup

1. Create a python environment with `python -m venv .venv`
2. Activate the environment `source .venv/Scripts/activate`
3. Install requirements `pip install -r requirements.txt`
4. Install Make (Windows: `choco install make` or `winget install GnuWin32.Make`; macOS: `brew install make`)
5. Create a `.env` file by following the examples set in `.env.example`. For OpenAI keys, use DSL account to procure one and monitor your usage.
6. Start oTree server `otree devserver`


### 2. Available Make Commands

```bash
make run                  # Run the OTree server
make install              # Install dependencies
make test-intro           # Run intro quiz tests
make test-simulation      # Run labor market simulation tests
make test-outro           # Run outro quiz tests
make test-all             # Run all tests
make help                 # Show available targets
```

### 3. How to play
1. Set the `SESSION_CONFIG_DEFAULTS` especially the `agent_player_ids` in `settings.py`.
2. Run the OTree server as mentioned in [Available Make Commands](#2-available-make-commands) section.
3. Open the URL in a browser.
4. Create a session and open each participant link separately.
5. The summary of the player decisions is stored in `_exports` folder.

### 4. Test Bot setup

The `labor_market/tests.py` outlines the test process as played by a bot. For steps such as `Get_Offers, Make_Offers and Choose_Effort`, we extract the state variables and build a prompt by reading the instructions from the corresponding `html` templates. To run tests with bot, use 
```bash
make test-all
``` 

## Otree Specific Concepts

- `participant.vars`: This is a per‑participant in‑memory store that persists across pages (and is saved in the session database). So the log lives with the participant record and can be accessed later in the session or exported. Can be used for logging/ saving reasoning.
- `session.vars`: Per‑session dict shared across all participants; can use this for shared state and debug info.
- `player` / `group` / `subsession`: Core model layers; `Player` is per participant per round, `Group` is per group per round, and `Subsession` is per round.
- `id_in_group`: Stable ID within a group; useful for role/agent mapping.
- `round_number`: Current round index; use for across‑round logic and summaries.
- `is_displayed()`: Page hook to conditionally show pages.
- `vars_for_template()`: Page hook to pass data into templates.
- `before_next_page()`: Page hook to persist decisions or compute outcomes.
- `get_timeout_seconds()`: Page hook to auto‑advance after N seconds. More outcomes or heuristic choices can be defined here. Setting `N>20` to allow the bot to generate the response.
- `timeout_submission`: Dict returned on timeout to auto‑submit form fields.
- `WaitPage` / `after_all_players_arrive()`: Synchronization and group‑level transitions.
- `live_method()`: Real‑time updates via websocket for live pages.
- `cu()` / `Currency`: oTree currency type; convert to `int/float` when serializing.
- `Bot` / `Submission`: Automated testing flow for simulating participant actions.