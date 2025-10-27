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

- `Intro a Regresion Lineal.ipynb`: Jupyter notebook covering Linear Regression concepts and implementation
- `Intro a Regresion Logistica.ipynb`: Jupyter notebook focusing on Logistic Regression analysis
- `requirements.txt`: List of Python packages required for this project
- `SQLite_databases_for_learning_data_science/`: Directory containing various SQLite databases for practice

## Tools and Technologies

- Python (3.x recommended)
- Jupyter Notebook
- Data Analysis Libraries:
  - Pandas (≥2.3.1)
  - Plotly (≥6.3.0)
  - Scikit-learn (≥1.7.1)
  - Category Encoders (≥2.8.1)
  - SciPy (≥1.16.1)
  - NumPy (≥2.3.2)

## Installation Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/jorgermzg15/predictive-models-intro.git
   cd predictive-models-intro
   ```

2. Create a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv .venv
   source .venv/bin/activate

   # On Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

5. Open either `Intro a Regresion Lineal.ipynb` or `Intro a Regresion Logistica.ipynb` in your browser and start learning!

## Troubleshooting

If you encounter any issues:

1. Make sure your virtual environment is activated (you should see `(.venv)` in your terminal)
2. Try upgrading pip before installing requirements:
   ```bash
   pip install --upgrade pip
   ```
3. If you have problems with any visualization, make sure Plotly is properly installed:
   ```bash
   pip install plotly --upgrade
   ```
4. If you encounter kernel issues in Jupyter:
   ```bash
   python -m ipykernel install --user
   ```

## For Students

This repository is designed to be a learning resource for predictive modeling techniques. Each notebook is structured to build upon fundamental concepts. Make sure to:

1. Follow the installation instructions carefully
2. Execute the notebook cells in order
3. Complete any exercises or challenges provided
4. Experiment with the code and parameters to deepen your understanding
5. Make use of the provided SQLite databases for practice

## License

This project is available for educational purposes. Feel free to use and learn from it!
