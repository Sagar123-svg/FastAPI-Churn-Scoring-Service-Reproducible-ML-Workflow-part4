# D2C Customer Churn Scoring Service & Automation Pipeline

## Project Overview
This repository contains a high-performance, independent FastAPI application that exposes machine learning inference endpoints to return customer churn risk metrics to internal CRM execution platforms.

## Repository Layout
* `app/main.py`: Core FastAPI service implementation containing Pydantic data schemas and endpoints logic.
* `train_model.py`: Script to generate production-ready mock model artifacts.
* `test_api.py`: Automated integration and parameter verification test matrix.
* `monitoring_plan.md`: Post-deployment operational monitoring rules and responsible-use framework.
* `requirements.txt`: Python package configuration manifest.

## Local Setup & Run Execution Guide

1. Ensure Python 3.10+ is installed on your computer.
2. Initialize and install project requirements:
   ```bash
   pip install -r requirements.txt
