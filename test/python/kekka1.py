import numpy as np
from plotly import graph_objects as go
from matplotlib import colors

class Graph():
    def __init__(self):
        pass

    def _unique_px(self, px, value, hue):
        val_list = [[i,0,0] for i in value]
        hue_list = [[i,0,0] for i in hue]
        gti_list = np.stack([px, val_list, hue_list], 1)
        uniq_list = np.unique(gti_list, axis=0)
        return uniq_list

    def _than_min_area(self):
        pass
    
    def _get_scatter_value(self,uniq_px_list):
        blue = [i[0,0] for i in uniq_px_list]
        green = [i[0,0] for i in uniq_px_list]
        red = [i[0,0] for i in uniq_px_list]
        fvfm_value = [i[1,0] for i in uniq_px_list]
        return blue, green, red, fvfm_value
    
    def draw_3dscatter(self, x, y, z, value=None, bar_title=None):
        marker = {'size': 1}
        if value is not None:
            marker{'color': value}
            if bar_title is not None:
                marker['colorbar'] = {'title': bar_title}
        fig = go.Figure(
            data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=marker
            )]
        )
        return fig
    
    def draw_histogram(self):
        pass
