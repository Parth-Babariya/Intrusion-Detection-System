
# Intrusion Detection System (IDS)

An open, production-oriented Intrusion Detection System (IDS) demonstrating tabular ML for network-flow classification, model explainability, and a reusable inference pipeline.

## Overview

This repository demonstrates an end-to-end IDS pipeline: data preprocessing, feature engineering, model training (Random Forest), model serialization, inference pipeline, and explainability using SHAP.

Key outcomes:
- Reusable inference pipeline at `src/fml_project/pipeline.py`.
- Saved model artifacts under `FML Project/` for demonstration.
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
- A previously circulated "Autoencoder + Random Forest: 89%" result was not found in the saved notebook outputs; to verify that result, reproduce the experiment and publish the evaluation artifact (recommended).

Notes on metrics:
- For robust claims, prefer cross-validation or repeated runs and report mean ± std.
- For imbalanced data, include per-class metrics and macro averages.

## Dataset

Expect a CSV of tabular network flows with fields such as `id`, `proto`, `service`, `state`, `spkts`, `dpkts`, etc. Add a small `FML Project/sample.csv` for quick local testing.

## Contributing

- Contributions are welcome. Add unit tests under `tests/` and include reproducible steps for any new experiments.
- Consider a CI workflow (GitHub Actions) to run `pytest` on push.

## License & Contact

- Author: Parth Babariya
- Repo: https://github.com/Parth-Babariya/Intrusion-Detection-System

