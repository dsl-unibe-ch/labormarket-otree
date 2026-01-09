# First Steps

1. Create a python environment with `python -m venv .venv`
2. Activate the environment `source .venv/Scripts/activate`
3. Install requirements `pip install -r requirements.txt`
4. Install Makefile.
   1. For Windows, `choco install make`
5. Start Otree server `otree devserver` 

# Extract Database Schema
1. Make sure that there is persistent data in the database (otherwise start the session and play the game).
2. Run `make get-schema` to render the Markdown file of the schema with teh contents. 