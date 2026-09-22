# Funciones de modelado: ajustar, evaluar y diagnosticar modelos OLS
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor


def ajustar_ols(X_train, y_train):
    """Ajusta un modelo OLS (agrega la constante automáticamente)."""
    return sm.OLS(y_train, sm.add_constant(X_train)).fit()


def predecir(results, X):
    """Predice con un modelo OLS ajustado con ajustar_ols()."""
    return results.predict(sm.add_constant(X))


def evaluar_modelo(nombre, results, X_test, y_test):
    """Imprime y regresa las métricas del modelo en el conjunto de prueba."""
    y_pred = predecir(results, X_test)
    metricas = {
        'modelo': nombre,
        'n_variables': X_test.shape[1],
        'R² ajustado (train)': round(results.rsquared_adj, 4),
        'R² (test)': round(r2_score(y_test, y_pred), 4),
        'RMSE (test)': round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
    }
    print(f"{nombre}: R² test = {metricas['R² (test)']} | RMSE test = {metricas['RMSE (test)']}")
    return metricas


def calcular_vif(X):
    """VIF de cada variable, de mayor a menor (se calcula con constante, igual que el modelo)."""
    X_const = sm.add_constant(X)
    vif = pd.DataFrame({
        'variable': X.columns,
        'VIF': [variance_inflation_factor(X_const.values, i + 1) for i in range(X.shape[1])],
    })
    return vif.sort_values('VIF', ascending=False).round(2).reset_index(drop=True)
