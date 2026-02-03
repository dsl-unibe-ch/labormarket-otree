.PHONY: run test install get-schema extract-db-data extract-instructions build-prompt prepare-to-play run-agent

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  run                  - Run the OTree server"
	@echo "  test                 - Run the tests"
	@echo "  install              - Install the dependencies"
	@echo "  get-schema           - Extract database schema to Markdown"
	@echo "  extract-db-data      - Extract all session data to JSON"
	@echo "  extract-instructions - Extract and concatenate instruction files"
	@echo "  build-prompt         - Build LLM prompt for agent (usage: make build-prompt PLAYER=1)"
	@echo "  prepare-to-play      - Extract schema, data, and instructions"
	@echo "  run-agent            - Run agent example (requires OPENAI_API_KEY) (usage: make run-agent PLAYER=1)"

run:
	otree devserver

install:
	pip install -r requirements.txt

test-intro:
	otree test test_intro

test-simulation:
	otree test test_simulation

test-outro:
	otree test test_outro

test-all:
	otree test test_all