.DEFAULT_GOAL := help
PYTHON := python
DBT_DIR := dbt_project

.PHONY: help install generate warehouse transform model export test all

help:
	@echo "Available commands:"
	@echo "  make install    Install Python dependencies"
	@echo "  make generate   Generate reproducible synthetic source data"
	@echo "  make warehouse  Load generated CSV files into DuckDB"
	@echo "  make transform  Run dbt models and data tests"
	@echo "  make model      Train and score the explainable risk model"
	@echo "  make export     Create Power BI-ready exports"
	@echo "  make test       Run Python tests"
	@echo "  make all        Run the complete pipeline"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

generate:
	$(PYTHON) -m src.generate_synthetic_data

warehouse:
	$(PYTHON) -m src.load_to_duckdb

transform:
	cd $(DBT_DIR) && dbt deps && dbt build

model:
	$(PYTHON) -m src.train_risk_model
	$(PYTHON) -m src.score_students

export:
	$(PYTHON) -m src.export_for_powerbi

test:
	pytest -q

all: generate warehouse transform model export test
