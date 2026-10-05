# Funciones de machine learning: evaluar y diagnosticar modelos de scikit-learn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.tree import plot_tree


def evaluar_regresion(nombre, y_true, y_pred):
    """Imprime y regresa R², RMSE y MAE de un modelo de regresión."""
    metricas = {
        'modelo': nombre,
        'R²': round(r2_score(y_true, y_pred), 4),
        'RMSE': round(np.sqrt(mean_squared_error(y_true, y_pred)), 4),
        'MAE': round(mean_absolute_error(y_true, y_pred), 3),
    }
    print(f"{nombre}: R² {metricas['R²']} | RMSE {metricas['RMSE']} | MAE {metricas['MAE']}")
    return metricas


def escalar(X_train, X_test):
    """Estandariza (media 0, desviación 1) ajustando sólo con train. Regresa ambos DataFrames."""
    from sklearn.preprocessing import StandardScaler

    escalador = StandardScaler().fit(X_train)
    X_train_s = pd.DataFrame(escalador.transform(X_train), columns=X_train.columns, index=X_train.index)
    X_test_s = pd.DataFrame(escalador.transform(X_test), columns=X_test.columns, index=X_test.index)
    return X_train_s, X_test_s


def plot_curva_k(k_values, scores, metrica='RMSE', menor_es_mejor=True):
    """Desempeño de validación cruzada para cada valor de k en KNN."""
    k_values, scores = list(k_values), list(scores)
    mejor = k_values[int(np.argmin(scores) if menor_es_mejor else np.argmax(scores))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=k_values, y=scores, mode='lines+markers',
        line=dict(color='steelblue', width=3), marker=dict(size=7), name=f'{metrica} (CV)'
    ))
    fig.add_vline(x=mejor, line_dash='dash', line_color='red', annotation_text=f'mejor k = {mejor}')
    fig.update_layout(
        title=f'Elección de k — {metrica} de validación cruzada',
        xaxis_title='k (número de vecinos)', yaxis_title=f'{metrica} (validación cruzada)',
        template='plotly_white', width=900, height=450
    )
    fig.show()
    return mejor


def plot_curva_complejidad(valores, score_train, score_test, parametro='max_depth', metrica='R²'):
    """Desempeño en entrenamiento vs prueba al aumentar la complejidad: así se ve el sobreajuste."""
    datos = pd.DataFrame({parametro: list(valores) * 2,
                          metrica: list(score_train) + list(score_test),
                          'conjunto': ['Entrenamiento'] * len(score_train) + ['Prueba'] * len(score_test)})

    fig = px.line(
        datos, x=parametro, y=metrica, color='conjunto', markers=True,
        title=f'Sobreajuste: {metrica} según {parametro}', template='plotly_white',
        color_discrete_map={'Entrenamiento': 'steelblue', 'Prueba': 'tomato'}
    )
    fig.update_layout(width=900, height=450)
    fig.show()


def plot_importancias(modelo, columnas, top_n=None):
    """Importancia de cada variable en un modelo basado en árboles."""
    imp = pd.Series(modelo.feature_importances_, index=columnas).sort_values(ascending=True)
    if top_n:
        imp = imp.tail(top_n)

    fig = px.bar(
        x=imp.values, y=imp.index, orientation='h', text_auto='.3f',
        labels={'x': 'Importancia (reducción de impureza)', 'y': ''},
        title='Importancia de variables', template='plotly_white'
    )
    fig.update_layout(width=800, height=450)
    fig.show()
    return imp.sort_values(ascending=False)


def plot_arbol(modelo, columnas, max_depth=3, class_names=None):
    """Dibuja los primeros niveles del árbol para poder leer sus reglas."""
    fig, ax = plt.subplots(figsize=(22, 9))
    plot_tree(
        modelo, max_depth=max_depth, feature_names=list(columnas), class_names=class_names,
        filled=True, rounded=True, fontsize=9, impurity=False, ax=ax
    )
    ax.set_title(f'Árbol de decisión — primeros {max_depth} niveles', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
