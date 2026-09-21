import plotly.express as px

def plot_correlation(corr_matrix):
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='hot',
        title='Matriz de Correlación'
    )

    fig.show()
