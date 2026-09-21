# Predictive Models Introduction

This repository contains Jupyter Notebooks focused on predictive modeling techniques, specifically covering Linear and Logistic Regression. The project is designed to help students understand and implement fundamental predictive modeling concepts.

## Project Overview

The project includes implementation and analysis of various predictive modeling techniques, such as:

- Linear Regression Analysis
- Logistic Regression
- Model Evaluation and Validation
- Statistical Analysis and Interpretation
- Data Visualization and Exploration

## Project Structure

Mirrors the students repo ([linear_regression_intro_students](https://github.com/jorgermzg15/linear_regression_intro_students)): same file names, but here every notebook is solved.

**Linear regression lab (session 1)**
- `fundamentos_regresion_lineal.ipynb`: Theory — OLS, coefficients and assumptions
- `mpg_case/regression_on_mpg.ipynb`: 🎯 3-hour lab — EDA, simple and multiple regression, VIF + p-values and RFECV

**Backup cases**
- `diamonds_case/`: EDA, OLS, KNN and Decision Tree regression on the diamonds dataset
- `california_case/`: Variable selection with VIF and p-values (California Housing)

**Classification (upcoming sessions)**
- `Intro a Regresion Logistica.ipynb`: Logistic Regression analysis
- `Intro Modelos de Clasificación.ipynb`: Introduction to classification models

**Environment**
- `pyproject.toml` / `uv.lock`: Project dependencies and the exact pinned versions
- `.python-version`: Exact Python version used everywhere
- `.devcontainer/`: GitHub Codespaces / Dev Container configuration

The MPG, diamonds OLS and California notebooks start with a "Funciones auxiliares de visualización" cell: run it once and then just call the plotting functions.

The SQLite databases are downloaded automatically by the notebooks (they are not versioned).

## Tools and Technologies

- Python 3.14 (exact version in `.python-version`)
- [uv](https://docs.astral.sh/uv/) to manage Python and dependencies
- Jupyter Notebooks (VS Code + Jupyter extension)
- pandas, NumPy, SciPy, scikit-learn, statsmodels, Plotly, Matplotlib, Category Encoders

## Environment

The local environment and GitHub Codespaces are built from the same files, so they are identical:

- `.python-version` pins the exact Python version (installed by uv, same build on every machine).
- `uv.lock` pins the exact version of every package.
- Codespaces runs `uv sync --frozen` when the container is created, which is the same command used locally.

### Option A: GitHub Codespaces (recommended)

Click **Code → Codespaces → Create codespace on main**. When the setup finishes, open any notebook and select the `.venv` kernel.

### Option B: Local

1. Install uv:
   ```bash
   # macOS
   brew install uv

   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Clone this repository and create the environment:
   ```bash
   git clone https://github.com/jorgermzg15/predictive-models-intro.git
   cd predictive-models-intro
   uv sync --frozen
   ```

3. Open the folder in VS Code and select the `.venv` interpreter/kernel in the notebooks.

### Updating dependencies (maintainer)

```bash
uv lock --upgrade   # resolve the newest compatible versions
uv sync --frozen    # apply them locally
```

Commit `uv.lock` (and `.python-version` if you change it). Codespaces will pick up the same versions on the next rebuild.

## Troubleshooting

1. Make sure the notebook kernel is the project's `.venv` (not a Conda/Anaconda environment).
2. If the environment gets out of sync, recreate it:
   ```bash
   rm -rf .venv
   uv sync --frozen
   ```
3. In Codespaces, if something breaks after changing `.devcontainer/`, run **Codespaces: Rebuild Container** from the command palette.

## For Students

This repository is designed to be a learning resource for predictive modeling techniques. Each notebook is structured to build upon fundamental concepts. Make sure to:

1. Follow the environment instructions carefully
2. Execute the notebook cells in order
3. Complete any exercises or challenges provided
4. Experiment with the code and parameters to deepen your understanding

## License

This project is available for educational purposes. Feel free to use and learn from it!

## Database Credits

The SQLite databases used in this project are sourced from the [SQLite Databases for Learning Data Science](https://github.com/davidjamesknight/SQLite_databases_for_learning_data_science) repository by David James Knight.