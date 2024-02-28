from plotly import graph_objects as go
from plotly.subplots import make_subplots


def show_sctter3d(fig1, fig2, fig3):
    fig = make_subplots(
        rows=1, cols=3,
        specs=[
            [{'type': 'scene'}, {'type': 'scene'}, {'type': 'xy'}]
        ]
    )
    fig.add_trace(fig1, row=1, col=1)
    fig.add_trace(fig2, row=1, col=2)
    fig.add_trace(fig3, row=1, col=3)
    fig.show()