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

Mirrors the students repo ([modelos-predictivos-students](https://github.com/jorgermzg15/modelos-predictivos-students)): same file names, but here every notebook is solved.

**Session 1 — Linear regression**
- `01-regresion-lineal/fundamentos.ipynb`: Theory — OLS, coefficients and assumptions
- `01-regresion-lineal/caso_mpg.ipynb`: 🎯 3-hour lab — EDA, simple and multiple regression, VIF + p-values and RFECV
- `01-regresion-lineal/slides/`: Slides for the session

Sessions 2-4 (KNN, decision trees, classification) get their own numbered folder as they are built.

**Extra material** (backup cases and instructor-only notebooks)
- `extra/diamonds/`: EDA, OLS, KNN and decision tree regression on the diamonds dataset
- `extra/california/`: Variable selection with VIF and p-values (California Housing)
- `extra/clasificacion/`: Logistic regression and intro to classification models

**Environment**
- `pyproject.toml` / `uv.lock`: Project dependencies and the exact pinned versions
- `.python-version`: Exact Python version used everywhere
- `.devcontainer/`: GitHub Codespaces / Dev Container configuration

The MPG, diamonds OLS and California notebooks start with a "Funciones auxiliares de visualización" cell: run it once and then just call the plotting functions.

The SQLite databases are downloaded automatically by the notebooks (they are not versioned).

## Claude Code skills (instructor)

`.claude/skills/` contains project skills for [Claude Code](https://claude.com/claude-code) that encode how this course is built. Invoke them with `/<name>` or just describe the task:

| Skill | What it does |
|---|---|
| `/crear-laboratorio` | Builds a new 3-hour lab as a notebook pair: solved version (here) + student template (students repo), from one definition |
| `/sincronizar-template` | Propagates changes between the solved notebook and the template without leaking solutions; keeps plotting helpers identical everywhere |
| `/auditar-curso` | Audits both repos: local ↔ Codespaces parity, latest dependencies, notebooks run, conceptual errors, READMEs |
| `/revisar-notebook-novatos` | Reviews a notebook from a beginner's perspective and proposes a friendlier structure |

Shared course conventions live in `.claude/skills/crear-laboratorio/references/convenciones.md`; the canonical helper code lives in `.claude/skills/crear-laboratorio/assets/`.

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