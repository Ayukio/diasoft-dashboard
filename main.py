from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly.express as px
from src.components.layout import create_layout
import pandas as pd
from bs4 import BeautifulSoup
import requests
from src.components.graphs_creator import ofr, balance_asset_structure, balance_asset_structure_col_names, balance_passive_structure, balance_passive_structure_col_names, odds_rises, odds_rises_col_names, odds_saldo
from src.components.layout import THEME, OFR_THEME


# -------------------------CREATE APP--------------------------------------
app = Dash(
        __name__,
    external_stylesheets=[BOOTSTRAP],
    routes_pathname_prefix='/dash/'
    )
app.title = "Diasoft dashboard"
app.layout = create_layout(app)


# ------------------------------CALLBACKS---------------------------------
@app.callback(
    Output('ofr_line_graph', 'figure'),
    [Input(component_id='radio', component_property='value'),
      Input(component_id='ofr-category-selector', component_property='value')
     ]
   
)
def build_ofr_graph(chart_type, selected_categories):
    if chart_type == 'Гистограмма':
        # Create a line chart with selected categories
        fig = px.bar(
        data_frame=ofr,
        x='Год',
        y=selected_categories,
        barmode='group',
        width=750,
        height=620,
        color_discrete_sequence=OFR_THEME
        ).update_layout(
             bargroupgap=0.1,
            legend_title_text='',
            xaxis_title="Год", 
            yaxis_title="Тыс. руб.",
            plot_bgcolor='#FFFFFF',
            legend=dict(
            orientation="h",
            entrywidth=400,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=16,
            ),
        )).update_yaxes(showline=True, linewidth=1, linecolor='#e9e9e9', gridcolor='#e9e9e9')
    else:
        fig = px.line(
        data_frame=ofr,
        x='Год',
        y=selected_categories,
        markers=True,
        width=750,
        height=620,
        color_discrete_sequence=OFR_THEME,
        ).update_layout(
            
            plot_bgcolor='#FFFFFF',
            legend_title_text='', 
            xaxis_title="Год", 
            yaxis_title="Тыс. руб.",
            legend=dict(
            orientation="h",
            entrywidth=300,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=16,
            ),
                )).update_traces(line=dict(width=4)).update_xaxes(showline=True, linewidth=1, linecolor='#e9e9e9', gridcolor='#e9e9e9').update_yaxes(showline=True, linewidth=1, linecolor='#e9e9e9', gridcolor='#e9e9e9')
    
    return fig

        
@app.callback(
    [Output('asset_graph', 'figure'), Output('capital_graph', 'figure')],
    [Input(component_id='year-balance-dropdown', component_property='value')]
)
def build_pie_graph(year):
    filtered_asset_data = list(balance_asset_structure[balance_asset_structure['Год'] == year].values.tolist()[0][:-1])

    asset = px.pie(
        names=balance_asset_structure_col_names[:-1], 
        values=filtered_asset_data, 
        hole = 0.7,
        color_discrete_sequence=THEME
        ).update_layout(
            
    legend=dict(
            orientation="h",
            entrywidth=300,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=18,
            ),
                ),
    autosize=False,
    height=620,
    width=560,
    font=dict(
        size=18,
        
    ),
    title={
        'text': "Актив",
        'y':0.96,
        'x':0.15,
        'xanchor': 'center',
        'yanchor': 'top'}
    )

    filtered_passive_data = list(balance_passive_structure[balance_passive_structure['Год'] == year].values.tolist()[0][:-1])

    passive = px.pie(
        names=balance_passive_structure_col_names[:-1], 
        values=filtered_passive_data, 
         hole = 0.7,
        color_discrete_sequence=THEME
        ).update_layout(
            
    legend=dict(
            orientation="h",
            entrywidth=300,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=18,
            ),
                ),
    autosize=False,
    height=620,
    width=560,
    font=dict(
        size=18,
        
    ),
    title={
        'text': "Пассив",
        'y':0.96,
        'x':0.15,
        'xanchor': 'center',
        'yanchor': 'top'}
    )

    return asset, passive


@app.callback(
    # [Output('odds_saldo', 'figure'), Output('odds_postup', 'figure')],
     Output('odds_saldo', 'figure'),
    [Input(component_id='year-odds-dropdown', component_property='value')]
)
def build_pie_graph(year):
    filtered_saldo_data = odds_saldo[odds_saldo['Год'] == year]

    saldo = px.bar(
        data_frame=filtered_saldo_data,
        y=odds_saldo.columns[:-1],
        barmode='group',
        color_discrete_sequence=THEME
        ).update_layout(
            bargroupgap=0.2,
            xaxis={'showgrid': False,
                   'visible': False,
                'showticklabels': False},
            yaxis={'showgrid': False,
                   'visible': False,
                'showticklabels': False},
            plot_bgcolor='#FFFFFF',
            margin=dict(l=0, r=0, b=0, t=15),
            legend_x=-1, 
            legend_y=0.5, 
            autosize=False, 
            height=320, 
            width=580,
            legend_title = '',
            title={
                'text': "Сальдо",
                'y':0.9,
                'x':0.2,
                'xanchor': 'center',
                'yanchor': 'top'},
                font=dict(
                size=16,
            ),
        ).update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='#e9e9e9')
    

    filtered_rises_data = list(odds_rises[odds_rises['Год'] == year].values.tolist()[0][:-1])

    rises = px.pie(
        names=odds_rises_col_names[:-1], 
        values=filtered_rises_data, 
        hole = 0.4,
        color_discrete_sequence=THEME
        ).update_layout(
        # legend_title_text=legend_title,
        legend_x=-3, legend_y=0.5,
        autosize=False,
        height=320,
        width=580,
        font=dict(
            size=16,
        ),
        title={
            'text': "Поступления",
            'y':0.9,
            'x':0.25,
            'xanchor': 'center',
            'yanchor': 'top'}
        )

        
    # return saldo, rises
    return saldo


if __name__ == "__main__":
    app.run_server(debug=True)
