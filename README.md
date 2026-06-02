Intrusion Detection System — Recruiter-Friendly Overview

This project implements an end-to-end Intrusion Detection System (IDS) using classical machine learning. It demonstrates data preprocessing, feature engineering, model training (Random Forest), model serving in a simple pipeline, and explainability with SHAP.

Why this project matters
- **Real-world problem:** Detects anomalous/attack traffic from network logs.
- **Production-oriented:** Includes a repeatable pipeline, saved model artifacts, and database loading step.
- **Explainability:** Uses SHAP to surface which features drive each attack prediction.
- **Skills showcased:** Data engineering, ML modeling, feature engineering, model serialization, SQL integration, and reproducible code organization.

Highlights (for recruiters)
- **Clear separation of concerns:** `src/fml_project/pipeline.py` contains modular functions (`load_models`, `transform_and_predict`, `explain_attacks`, `load_to_db`, `run_pipeline`).
- **Reproducible environment:** `requirements.txt` captures exact runtime dependencies.
- **Artifacts included:** `FML Project/random_forest_model.pkl` and `FML Project/scaler.pkl` (used for inference).
- **Tests & CI-ready:** simple test scaffold under `tests/` to extend for CI.

Repository structure
- **Source:** `src/fml_project/` (production code)
- **Notebooks:** `FML Project/` contains exploration notebooks and reports
- **Models:** `FML Project/random_forest_model.pkl`, `FML Project/scaler.pkl`
- **Tests:** `tests/`
- **Docs:** this `README.md`

Quickstart (run locally)
1. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the inference pipeline on a CSV file (example):

```bash
python -m src.fml_project.pipeline
# or specify input and DB connection
python -c "from src.fml_project.pipeline import run_pipeline; run_pipeline(input_csv='FML Project/sample.csv', db_connection_str=None)"
```

What to customize
- `input_csv`: point to your incoming network logs CSV
- `model_path` / `scaler_path`: swap to your latest trained artifacts
- `db_connection_str`: provide a PostgreSQL connection string to enable `load_to_db`

How this helps recruiters evaluate you
- **Readable code**: modular functions with clear names make it easy to review your engineering choices.
- **Impact-first README**: summarizes the problem, your contributions, and how to run the project in under a minute.
- **Interview talking points:** data challenges, feature selection, model evaluation, explainability trade-offs, and deployment considerations.

Next steps (recommended)
- Add a short `CONTRIBUTING.md` describing how you expect collaborators to run tests and linting.
- Add minimal unit tests for `transform_and_predict` using a tiny synthetic CSV sample.
- Add GitHub Actions to run tests on push (I can scaffold this for you).

Contact / Attribution
- Author: Parth Babariya
- Repo: https://github.com/Parth-Babariya/Intrusion-Detection-System

License
- If you'd like, I can add an open-source license (MIT recommended for recruiters).

If you want, I can now: add CI, write a unit test, or add a one-page PDF summary suitable for attaching to applications.

Problem statement
-----------------
Network operators need fast, reliable detection of malicious or anomalous traffic from streaming logs. Manual inspection doesn't scale and blind models without explainability reduce trust.

What this project solves
-----------------------
- Detects likely attack flows vs normal traffic from tabular network logs.
- Produces per-row explanations (top contributing feature) so analysts can triage alerts quickly.
- Provides a repeatable pipeline pattern for inference, storage, and reporting.

Algorithms & models
-------------------
- Random Forest classifier (scikit-learn) — robust, interpretable at feature-level and effective for tabular data.
- MinMaxScaler for numeric feature scaling (saved as `scaler.pkl`).
- SHAP (TreeExplainer) for model-agnostic explanation of individual predictions.

Tech stack
----------
- Language: Python 3.8+
- Data: pandas, numpy
- ML: scikit-learn, joblib
- Explainability: shap
- Storage & infra: SQLAlchemy + PostgreSQL (optional load step)
- Dev tooling: Jupyter notebooks, pytest (tests/), Git, GitHub

Dataset (notes)
----------------
The repository expects tabular network logs (CSV) with common flow features such as `id`, `proto`, `service`, `state`, `spkts`, `dpkts`, and other statistics. Example file: `FML Project/sample.csv` (create for local testing).

Evaluation
----------
Training and evaluation were performed offline (not included in the pipeline module). Typical metrics to report: accuracy, precision, recall, F1-score, and confusion matrix for the attack class. Add evaluation notebooks under `FML Project/` to show model performance snapshots.

If you'd like, I can add a short `EVALUATION.md` with example metrics and the commands to reproduce them.
