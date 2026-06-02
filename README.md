Intrusion Detection System (FML Project)

This repository contains an intrusion detection pipeline using a Random Forest model.

Structure
- `src/fml_project/`: package containing the pipeline code
- `notebooks/`: Jupyter notebooks and experiments
- `tests/`: unit/integration tests
- `random_forest_model.pkl`, `scaler.pkl`: trained artifacts (do not commit secrets)

Quick start
1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the pipeline on a CSV file:

```bash
python -m src.fml_project.pipeline --input new_network_traffic.csv
```

Pushing to GitHub
- Initialize a git repo (if not already), add a remote, and push:

```bash
git init
git add .
git commit -m "Initial project structure"
git branch -M main
git remote add origin <your-git-url>
git push -u origin main
```

Replace `<your-git-url>` with your GitHub repository URL.
