# Funciones de clasificación: ajustar, evaluar y diagnosticar modelos de clasificación
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score, roc_curve)


def ajustar_logit(X_train, y_train):
    """Ajusta una regresión logística (agrega la constante automáticamente)."""
    return sm.Logit(y_train, sm.add_constant(X_train)).fit(disp=0)


def predecir_proba(results, X):
    """Probabilidad estimada de la clase positiva, entre 0 y 1."""
    return results.predict(sm.add_constant(X))


def razon_de_momios(results):
    """Coeficientes en log-odds, su razón de momios (odds ratio) y el p-value."""
    return pd.DataFrame({
        'coef (log-odds)': results.params.round(4),
        'razón de momios': np.exp(results.params).round(3),
        'p-value': results.pvalues.round(4),
    })


def evaluar_clasificador(nombre, y_true, y_pred):
    """Imprime y regresa exactitud, precisión, recall y F1."""
    metricas = {
        'modelo': nombre,
        'exactitud': round(accuracy_score(y_true, y_pred), 3),
        'precisión': round(precision_score(y_true, y_pred, zero_division=0), 3),
        'recall': round(recall_score(y_true, y_pred, zero_division=0), 3),
        'F1': round(f1_score(y_true, y_pred, zero_division=0), 3),
    }
    print(f"{nombre}: exactitud {metricas['exactitud']} | precisión {metricas['precisión']} "
          f"| recall {metricas['recall']} | F1 {metricas['F1']}")
    return metricas


def plot_tasa_por_categoria(df, columna, objetivo):
    """Proporción de la clase positiva dentro de cada categoría."""
    tasa = df.groupby(columna, as_index=False)[objetivo].mean()

    fig = px.bar(
        tasa,
        x=columna,
        y=objetivo,
        text_auto='.1%',
        title=f'Tasa de {objetivo} por {columna}',
        template='plotly_white'
    )
    fig.update_layout(yaxis_tickformat='.0%', yaxis_title=f'Tasa de {objetivo}', width=700, height=450)
    fig.update_xaxes(type='category')
    fig.show()


def plot_matriz_confusion(y_true, y_pred, etiquetas=('No', 'Sí'), title='Matriz de confusión'):
    """Aciertos y errores del clasificador: la diagonal son los aciertos."""
    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred),
        index=[f'Real: {e}' for e in etiquetas],
        columns=[f'Predicho: {e}' for e in etiquetas]
    )

    fig = px.imshow(cm, text_auto=True, color_continuous_scale='Blues', title=title)
    fig.update_layout(width=650, height=450)
    fig.show()


def plot_curva_roc(y_true, y_proba, title='Curva ROC'):
    """Compromiso entre verdaderos y falsos positivos al mover el umbral."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode='lines', name=f'Modelo (AUC = {auc:.3f})',
        line=dict(color='steelblue', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode='lines', name='Azar (AUC = 0.5)',
        line=dict(color='red', dash='dash')
    ))
    fig.update_layout(
        title=title,
        xaxis_title='Falsos positivos (1 − especificidad)',
        yaxis_title='Verdaderos positivos (recall)',
        template='plotly_white', width=700, height=550
    )
    fig.show()


def plot_metricas_por_umbral(y_true, y_proba):
    """Cómo cambian exactitud, precisión, recall y F1 según el umbral de decisión."""
    umbrales = np.arange(0.05, 0.96, 0.05)
    filas = []
    for u in umbrales:
        y_pred = (y_proba >= u).astype(int)
        filas.append({
            'umbral': round(u, 2),
            'exactitud': accuracy_score(y_true, y_pred),
            'precisión': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'F1': f1_score(y_true, y_pred, zero_division=0),
        })

    datos = pd.DataFrame(filas).melt(id_vars='umbral', var_name='métrica', value_name='valor')

    fig = px.line(
        datos, x='umbral', y='valor', color='métrica', markers=True,
        title='Métricas según el umbral de decisión', template='plotly_white'
    )
    fig.add_vline(x=0.5, line_dash='dash', line_color='gray', annotation_text='umbral por defecto')
    fig.update_layout(width=900, height=500)
    fig.show()


def plot_sigmoide():
    """La función que convierte cualquier número en una probabilidad entre 0 y 1."""
    z = np.linspace(-8, 8, 200)

    fig = px.line(
        x=z, y=1 / (1 + np.exp(-z)),
        labels={'x': 'z = β₀ + β₁x₁ + β₂x₂ + …', 'y': 'Probabilidad estimada'},
        title='Función sigmoide (logística)', template='plotly_white'
    )
    fig.add_hline(y=0.5, line_dash='dash', line_color='red', annotation_text='umbral 0.5')
    fig.add_vline(x=0, line_dash='dot', line_color='gray')
    fig.update_traces(line=dict(color='steelblue', width=3))
    fig.update_layout(width=800, height=450)
    fig.show()
