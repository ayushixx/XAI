# 8BIT Workforce Signal Engine

## Problem Context
Data-driven workforce intelligence for Data Science and Analytics. The project analyzes industry demand, junior skill requirements, and senior success traits to provide actionable insights.

## Architecture
The analytical pipeline strictly processes the 4 official SAS CU Hackathon datasets to build the 8BIT Signal Engine.
It uses modular Python components for cleaning, statistics, modeling, and signal aggregation.

## How to Reproduce
1. Ensure the 4 datasets are in `data/raw/`.
2. Run `pip install -r requirements.txt`.
3. Run `python run_pipeline.py`.
4. Outputs will be populated in `data/outputs/sas/`, `reports/figures/`, and `reports/models/`.

## SAS Integration
The outputs located in `data/outputs/sas/` are cleaned and formatted specifically for ingestion into SAS Visual Analytics and SAS Model Studio.
