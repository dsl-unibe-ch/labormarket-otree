# Labor Market oTree Experiment

An oTree experiment for studying decision-making in organizational labor market settings.

## Setup

### 1. Initial Setup

1. Create a python environment with `python -m venv .venv`
2. Activate the environment `source .venv/Scripts/activate`
3. Install requirements `pip install -r requirements.txt`
4. Install Make (Windows: `choco install make` or `winget install GnuWin32.Make`; macOS: `brew install make`)
5. Create a `.env` file by following the examples set in `.env.example`. For OpenAI keys, use DSL account to procure one and monitor your usage.
6. Start oTree server `otree devserver`
7. To run tests with bot, use `make test-all` 

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
