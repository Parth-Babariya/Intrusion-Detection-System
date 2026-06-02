
# Intrusion Detection System (IDS)

A concise, recruiter-focused overview and instructions for the Intrusion Detection System project.

## Overview

This repository demonstrates an end-to-end IDS pipeline: data preprocessing, feature engineering, model training (Random Forest), model serialization, inference pipeline, and explainability using SHAP.

Key outcomes:
- Reusable inference pipeline at `src/fml_project/pipeline.py`.
- Saved model artifacts under `FML Project/` for quick demos.
- Notebook-driven experiments and evaluation snapshots.

## Problem Statement

Network operators need fast, reliable detection of malicious or anomalous traffic. Manual triage doesn't scale and unexplainable models reduce analyst trust.

## Solution

We train a Random Forest classifier on tabular network flow features, use `MinMaxScaler` for numeric scaling, and SHAP for per-row explanations to help analysts triage alerts.

## Highlights (for recruiters)

- Clean package layout: `src/fml_project/` contains production-ready code.
- Reproducible environment: `requirements.txt` lists dependencies.
- Explainability: per-prediction SHAP explanations to support analyst workflows.

## Tech stack

- Python 3.8+
- pandas, numpy
- scikit-learn, joblib
- shap
- SQLAlchemy + PostgreSQL (optional data sink)

## Repository layout

- `src/fml_project/` — inference pipeline and helpers
- `FML Project/` — notebooks, example data, and saved models
- `tests/` — test scaffold to extend
- `requirements.txt`, `.gitignore`, `README.md`

## Quickstart

1. Create and activate a virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the pipeline on a CSV file (example):

```powershell
python -m src.fml_project.pipeline
# or run the orchestrator from Python
python -c "from src.fml_project.pipeline import run_pipeline; run_pipeline(input_csv='FML Project/sample.csv', db_connection_str=None)"
```

## Usage notes

- Replace `input_csv`, `model_path`, and `scaler_path` with your artifacts for production use.
- Set `db_connection_str` to a PostgreSQL DSN to enable `load_to_db`.

## Evaluation (from included notebooks)

- The notebooks `FML Project/Random_forest.ipynb` and `FML Project/fml-project_2.ipynb` report weighted averages in the classification reports: **precision 0.92, recall 0.90, F1-score 0.91** (weighted). This corresponds to a weighted F1 ≈ 0.91 on the held-out test split.
- The previously mentioned "Autoencoder + Random Forest: 89%" value was not found verbatim in saved notebook outputs; if this came from a different run, provide the output or I can reproduce the experiment and confirm.

Notes on metrics:
- For robust claims, prefer cross-validation or repeated runs and report mean ± std.
- For imbalanced data, include per-class metrics and macro averages.

## Dataset

Expect a CSV of tabular network flows with fields such as `id`, `proto`, `service`, `state`, `spkts`, `dpkts`, etc. Add a small `FML Project/sample.csv` for quick local testing.

## Contributing

- Add unit tests under `tests/` and consider a GitHub Actions workflow to run `pytest` on push.
- Prefer small, documented PRs and include reproducible steps for new experiments.

## License & Contact

- Author: Parth Babariya
- Repo: https://github.com/Parth-Babariya/Intrusion-Detection-System
- License: let me know if you want MIT added.

