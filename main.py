from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly.express as px
from src.components.layout import create_layout
import pandas as pd
from bs4 import BeautifulSoup
import requests
from src.components.graphs_creator import ofr
from src.components.layout import THEME


# def main() -> None:
app = Dash(
        __name__,
    external_stylesheets=[BOOTSTRAP],
    routes_pathname_prefix='/dash/'
    )
app.title = "Diasoft dashboard"
app.layout = create_layout(app)




    # ---------------------------------------------------------------
@app.callback(
    Output('ofr_line_graph', 'figure'),
    [Input(component_id='radio', component_property='value')]
)
def build_graph(value):
    if value == 'Гистограмма':
        return px.bar(
        data_frame=ofr,
        x='Год',
        y=ofr.columns,
        barmode='group',
        color_discrete_sequence=THEME
        ).update_layout(
            legend_title_text='Тип прибыли',
            xaxis_title="Год", 
            yaxis_title="Тыс. руб.",
            plot_bgcolor='#FFFFFF',
            legend=dict(
            orientation="h",
            entrywidth=130,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=16,
            ),
        )).update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='#e9e9e9')
    
    

    else:
        return px.line(
        data_frame=ofr,
        x='Год',
        y=ofr.columns,
        markers=True,
        color_discrete_sequence=THEME,
        ).update_layout(
            
            plot_bgcolor='#FFFFFF',
            legend_title_text='Тип прибыли', 
            xaxis_title="Год", 
            yaxis_title="Тыс. руб.",
            legend=dict(
            orientation="h",
            entrywidth=130,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=16,
            ),
                )).update_traces(line=dict(width=4)).update_xaxes(showline=True, linewidth=1, linecolor='white', gridcolor='#e9e9e9').update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='#e9e9e9')
        
    


if __name__ == "__main__":
    app.run_server(debug=True)
