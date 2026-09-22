# Funciones auxiliares de visualización
# Ejecuta esta celda una vez; después sólo llama a las funciones.
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def plot_distributions(df, columns, nbins=30):
    """Histograma con boxplot marginal para cada variable numérica."""
    for col in columns:
        fig = px.histogram(
            df,
            x=col,
            nbins=nbins,
            marginal='box',
            opacity=0.7,
            title=f'Distribución de {col}'
        )
        fig.update_layout(bargap=0.2)
        fig.show()


def plot_frequencies(df, columns, top_n=None):
    """Gráfica de barras con la frecuencia de cada categoría (top_n limita a las más comunes)."""
    for col in columns:
        freq = df[col].value_counts()
        if top_n:
            freq = freq.head(top_n)
        freq_df = freq.rename_axis(col).reset_index(name='Frecuencia')

        title = f'Frecuencias de {col}'
        if top_n and df[col].nunique() > top_n:
            title += f' (top {top_n})'

        fig = px.bar(freq_df, x=col, y='Frecuencia', title=title)
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        fig.show()


def plot_correlation_matrix(df, columns):
    """Mapa de calor con la correlación de Pearson entre las variables numéricas."""
    corr = df[columns].corr().round(2)
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        title='Matriz de Correlación'
    )
    fig.update_layout(width=750, height=650)
    fig.show()


def plot_pairplot(df, columns, color=None):
    """Matriz de dispersión (pairplot) entre las variables numéricas."""
    fig = px.scatter_matrix(
        df,
        dimensions=columns,
        color=color,
        title='Pairplot de Variables Numéricas',
        labels={col: col.capitalize() for col in columns}
    )
    fig.update_layout(width=1200, height=1200, title_font_size=20)
    fig.update_traces(diagonal_visible=True)
    fig.show()


def plot_simple_regression(x, y, results):
    """Dispersión de una variable vs el objetivo con la recta ajustada por un OLS de 1 variable."""
    b0, b1 = results.params.iloc[0], results.params.iloc[1]
    x_name = getattr(x, 'name', None) or 'x'
    y_name = getattr(y, 'name', None) or 'y'
    x_line = np.linspace(np.min(x), np.max(x), 100)

    fig = px.scatter(
        x=np.asarray(x),
        y=np.asarray(y),
        opacity=0.6,
        labels={'x': x_name, 'y': y_name},
        title=f'{y_name} = {b0:.2f} + ({b1:.4f}) · {x_name}',
        template='plotly_white'
    )
    fig.add_trace(go.Scatter(
        x=x_line,
        y=b0 + b1 * x_line,
        mode='lines',
        name='Recta OLS',
        line=dict(color='red', width=3)
    ))
    fig.show()


def plot_actual_vs_predicted(y_true, y_pred, title='Real vs Predicho'):
    """Valores reales vs predichos; un modelo perfecto cae sobre la diagonal roja."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    lo = min(y_true.min(), y_pred.min())
    hi = max(y_true.max(), y_pred.max())

    fig = px.scatter(
        x=y_true,
        y=y_pred,
        opacity=0.5,
        labels={'x': 'Valor real', 'y': 'Valor predicho'},
        title=title,
        template='plotly_white'
    )
    fig.add_shape(
        type='line', x0=lo, y0=lo, x1=hi, y1=hi,
        line=dict(color='red', dash='dash')
    )
    fig.show()


def plot_residuals(y_true, y_pred, title='Residuales vs Predicho'):
    """Residuales vs predichos; buscamos una nube sin patrón alrededor de 0."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)

    fig = px.scatter(
        x=y_pred,
        y=y_true - y_pred,
        opacity=0.5,
        labels={'x': 'Valor predicho', 'y': 'Residual (real − predicho)'},
        title=title,
        template='plotly_white'
    )
    fig.add_hline(y=0, line_dash='dash', line_color='red')
    fig.show()


def plot_rfecv(rfecv):
    """R² promedio de validación cruzada según el número de variables que conserva RFECV."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rfecv.cv_results_['n_features'],
        y=rfecv.cv_results_['mean_test_score'],
        mode='lines+markers',
        line=dict(color='steelblue', width=3),
        marker=dict(size=7),
        name='R² promedio (CV)'
    ))
    fig.update_layout(
        title='RFECV — R² según número de variables seleccionadas',
        xaxis_title='Número de variables',
        yaxis_title='R² (validación cruzada)',
        template='plotly_white',
        width=900, height=450
    )
    fig.show()
