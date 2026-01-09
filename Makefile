.PHONY: run test install get-schema

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  run - Run the OTree server"
	@echo "  test - Run the tests"
	@echo "  install - Install the dependencies"
	@echo "  get-schema - Create the database schema"

run:
	otree devserver

install:
	pip install -r requirements.txt

get-schema:
	python prompt_builder/schema_extractor.py