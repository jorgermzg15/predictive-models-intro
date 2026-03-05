import plotly.figure_factory as ff

def plot_correlation(corr_matrix):
    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale='hot',
        showscale=True,
        annotation_text=corr_matrix.values
    )

    fig.update_layout(
        title='Matriz de Correlación',
        yaxis=dict(autorange="reversed")
    )

    fig.show()