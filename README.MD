# Labor Market oTree Experiment

An oTree experiment for studying decision-making in organizational labor market settings.

## Setup

### 1. Initial Setup

1. Create a python environment with `python -m venv .venv`
2. Activate the environment `source .venv/Scripts/activate`
3. Install requirements `pip install -r requirements.txt`
4. Create a `.env` file. See example set in `.env.example`. 
   1. **Note** that you will need an OpenAI key to be saved in `.env`.
5. \\[Optional] : Install [Make](https://www.gnu.org/software/make/) tool 
   1. Windows: `choco install make` or `winget install GnuWin32.Make`
   2. MacOS: `brew install make`

### 2. How to play

1. Set the `SESSION_CONFIG_DEFAULTS` especially the `agent_player_ids` in `settings.py`. The `agent_player_ids` refer to the number of players that will be played by the LLM. **Note** that by default, 12 players are played by the bot.
2. Start oTree server with `otree devserver` or by make tool as described [here](#2-available-make-commands).
3. Open the URL in a browser.
4. Create a session.
5. Open each participant link individually. This is **important** to start the process for the bot.
6. As the game progresses, the player decisions per session with a `SESSION_ID` is automatically stored in `_exports` folder under `game_summary_{SESSION_ID}` and `reasoning_{SESSION_ID}`. 

### 3. Settings
1. Prompt Settings: The prompts for each stage in a period `make_offers`, `get_offers` and `choose_effort` are defined in the file `agent/prompts.py`. These can be modified to change the LLM behaviour.
2. The pages wait for 20 seconds to allow the LLM more than enough time to generate the response. It is defined in `settings.py` under `page_timeout_seconds_agent=20`. It may be possible to reduce the time for faster execution however please **note** that setting this value to a low number may **not** give the LLM sufficient time for response generation. 

### 4. Available Make Commands

```bash
make run                  # Run the OTree server
make install              # Install dependencies
make test-intro           # Run intro quiz tests
make test-simulation      # Run labor market simulation tests
make test-outro           # Run outro quiz tests
make test-all             # Run all tests
make help                 # Show available targets
```

### 5. Test Bot setup

The `labor_market/tests.py` outlines the test process as played by a bot. For steps such as `Get_Offers, Make_Offers and Choose_Effort`, we extract the state variables and build a prompt by reading the instructions from the corresponding `html` templates. To run tests with bot, use

```bash
make test-all
```


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


## Otree Specific Concepts

### Game Structure: Periods and Steps

The experiment is structured in two levels:

- **Periods**: The game consists of multiple periods. Each period is a complete cycle of the labor market interaction. The number of periods is configured in the session settings, and `round_number` tracks the current period index.
- **Steps within Each Period**: Each period consists of multiple sequential steps as outlined in the "High Level Description of the Steps" section above. These steps include the hiring phase (which itself repeats `C.HIRING_STEPS` times), matching, effort choice, and results display. Players progress through these steps in order within each period before moving to the next period.

### Core oTree Concepts

- `participant.vars`: This is a per‑participant in‑memory store that persists across pages (and is saved in the session database). So the log lives with the participant record and can be accessed later in the session or exported. Can be used for logging/ saving reasoning.
- `session.vars`: Per‑session dict shared across all participants; can use this for shared state and debug info.
- `player` / `group` / `subsession`: Core model layers; `Player` is per participant per period, `Group` is per group per period, and `Subsession` is per period.
- `id_in_group`: Stable ID within a group; useful for role/agent mapping.
- `round_number`: Current period index; use for across‑period logic and summaries.
- `is_displayed()`: Page hook to conditionally show pages.
- `vars_for_template()`: Page hook to pass data into templates.
- `before_next_page()`: Page hook to persist decisions or compute outcomes.
- `get_timeout_seconds()`: Page hook to auto‑advance after N seconds. More outcomes or heuristic choices can be defined here. Setting `N>20` to allow the bot to generate the response.
- `timeout_submission`: Dict returned on timeout to auto‑submit form fields.
- `WaitPage` / `after_all_players_arrive()`: Synchronization and group‑level transitions.
- `live_method()`: Real‑time updates via websocket for live pages.
- `cu()` / `Currency`: oTree currency type; convert to `int/float` when serializing.
- `Bot` / `Submission`: Automated testing flow for simulating participant actions.
