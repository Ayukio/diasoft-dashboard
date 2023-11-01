from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from bs4 import BeautifulSoup
import requests
from src.components.graphs_creator import kpi, kpi_col_names, balance_asset_structure, balance_asset_structure_col_names, balance_asset_structure_last_year, balance_passive_structure, balance_passive_structure_col_names, balance_passive_structure_last_year, ofr, odds_saldo, odds_saldo_col_names, odds_saldo_last_year, odds_rises, odds_rises_col_names, odds_rises_last_year

THEME = px.colors.qualitative.Vivid 

def create_layout(app: Dash) -> html.Div:
    
# ===========KPI КАРТОЧКИ===========
    def get_kpi_plot(label, kpi_title):
        fig1 = go.Figure(
                go.Scatter(
                    x=kpi.index,
                    y=kpi_title['values'],
                    mode='lines',
                    fill='tozeroy',
                    line_color=kpi_title['color'],
                    name='',
                    hoverinfo='skip',
                )
            )
        
        fig1.add_trace(
            go.Indicator(
                mode='number+delta',
                value=kpi_title['y'],
                title={'text': label + ', ₽',
                    'font': {'size': 20},
                    },
                number={
                        'suffix': ' млрд',
                        'font': {'size': 36},
                        },
                delta={'position': 'bottom',
                    'reference': kpi_title['yo'],
                    'relative': True,
                    "valueformat": ".2%",
                    'font': {'size': 20},
                    },
                domain={'y': [0, 0.7], 'x': [0.25, 0.75]},
            ))
        
        fig1.update_layout(
            xaxis={'showgrid': False,
                'showticklabels': False},
            yaxis={'showgrid': False,
                'showticklabels': False},
            plot_bgcolor='#FFFFFF',
            margin=dict(l=0, r=0, b=0, t=15),
            autosize=True,
        )

        return fig1


    bal = kpi.loc[:, kpi_col_names[0]].values
    prof = kpi.loc[:, kpi_col_names[1]].values
    rev = kpi.loc[:, kpi_col_names[2]].values
    tax = kpi.loc[:, kpi_col_names[3]].values

    kpis = {'Баланс': {'values': bal, 'y': float(f'{bal[-1]/(1000000):.3f}') , 'yo': float(f'{bal[-2]/(1000000):.3f}') , 'color': '#E2EFED'},
        'Прибыль': {'values': prof, 'y': float(f'{prof[-1]/(1000000):.3f}') , 'yo': float(f'{prof[-2]/(1000000):.3f}') , 'color': '#E5E4E2'}, 
        'Выручка': {'values': rev, 'y': float(f'{rev[-1]/(1000000):.3f}') , 'yo': float(f'{rev[-2]/(1000000):.3f}') , 'color': '#E6E6F8'}, 
        'Капитал': {'values': tax, 'y': float(f'{tax[-1]/(1000000):.3f}') , 'yo': float(f'{tax[-2]/(1000000):.3f}') , 'color': '#E0EAF5'}}
    
    for _, (k, v) in enumerate(kpis.items()):
        if k == 'Баланс': fig_bal = get_kpi_plot(k, v) 
        if k == 'Прибыль': fig_prof = get_kpi_plot(k, v)
        if k == 'Выручка': fig_rev = get_kpi_plot(k, v)
        if k == 'Капитал': fig_tax = get_kpi_plot(k, v)

# ===========БУХГАЛТЕРСКИЙ БАЛАНС===========

    balance_asset_structure_graph = px.pie(
        names=balance_asset_structure_col_names[:-1], 
        values=balance_asset_structure_last_year, 
        hole = 0.4,
        color_discrete_sequence=THEME
        )
    
    balance_asset_structure_graph.update_layout(
    legend_x=-1.7, 
    legend_y=0.5,
    autosize=False,
    height=320,
    width=580,
    font=dict(
        size=16,
        
    ),
    title={
        'text': "Актив в 2022",
        'y':0.9,
        'x':0.2,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    

    balance_passive_structure_graph =  px.pie(
        names=balance_passive_structure_col_names[:-1], 
        values=balance_passive_structure_last_year, 
         hole = 0.4,
        color_discrete_sequence=THEME
        
        )
    balance_passive_structure_graph.update_layout(
        title={
            'text': "Пассив в 2022",
            'y':0.9,
            'x':0.2,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
        size=16,
        ),
        legend_x=-1.7, 
        legend_y=0.5, 
        autosize=False, 
        height=320, 
        width=580
    )
    
# ===========ОФР===========
    ofr_graph = px.bar(
        data_frame=ofr,
        x='Год',
        y=ofr.columns,
        barmode='group',
        color_discrete_sequence=THEME
    )

    ofr_graph.update_layout(
        legend_title_text='Вид показателя',
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
    ))
    

    ofr_line_graph = px.line(
        data_frame=ofr,
        x='Год',
        y=ofr.columns,
        markers=True,
        color_discrete_sequence=THEME
        )
    
    ofr_line_graph.update_layout(
        legend_title_text='Вид прибыли', 
        xaxis_title="Год", 
        yaxis_title="Тыс. руб.",
        legend=dict(
        orientation="h",
        entrywidth=70,
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
            ))
    

# ===========ОДДС. Сальдо от операций===========
    odds_saldo_graph = px.bar(
        data_frame=odds_saldo_last_year,
        y=odds_saldo.columns[:-1],
        barmode='group',
        color_discrete_sequence=THEME
        )
    
    odds_saldo_graph.update_layout(
            xaxis={'showgrid': False,
                   'visible': False,
                'showticklabels': False},
            yaxis={'showgrid': False,
                   'visible': False,
                'showticklabels': False},
            plot_bgcolor='#FFFFFF',
            margin=dict(l=0, r=0, b=0, t=15),
            legend_x=-1.7, 
            legend_y=0.5, 
            autosize=False, 
            height=320, 
            width=580,
            legend_title = '',
            title={
                'text': "Сальдо в 2022",
                'y':0.9,
                'x':0.2,
                'xanchor': 'center',
                'yanchor': 'top'},
                font=dict(
                size=16,
            ),
        )
    odds_saldo_graph.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='#e9e9e9')
    
# ===========ОДДС. Поступления от операций===========
    odds_rises_graph = px.pie(
        names=odds_rises_col_names[:-1], 
        values=odds_rises_last_year, 
        hole = 0.4,
        color_discrete_sequence=THEME
        )
    
    odds_rises_graph.update_layout(
        legend_x=-3, legend_y=0.5,
        autosize=False,
        height=320,
        width=580,
        font=dict(
            size=16,
        ),
        title={
            'text': "Поступления в 2022",
            'y':0.9,
            'x':0.25,
            'xanchor': 'center',
            'yanchor': 'top'}
)
    


    
# ===========Разметка страницы===========

    return html.Div(
        className="app-div",
        style = {'margin': 'auto', 'width': '1200px', 'padding-top': '30px',
 
    },
        children=[
            dbc.Row(
            [
                dbc.Row(
                   [
                        dcc.Graph(id='balance-indicator',
                                  figure = fig_bal,
                                style={
                                    'height': '95%',
                                    'width': '23%',
                                }),
                        dcc.Graph(id='profit-indicator',
                                  figure = fig_prof,
                                style={
                                    'height': '95%',
                                    'width': '23%',

                                }),
                        dcc.Graph(id='revenue-indicator',
                                  figure = fig_rev,
                                style={
                                    'height': '95%',
                                    'width': '23%',
                                }),
                        dcc.Graph(id='tax-indicator',
                                  figure = fig_tax,
                                style={
                                    'height': '95%',
                                    'width': '23%',
                                }),
                        
                    ],
                    style={
                        'height': '14rem',
                        'display': 'flex',
                        'flex-direction': 'row',
                        'justify-content': 'space-between',
                        
                    },
                ),
            ],
        ),
            html.H4('Бухгалтерский баланс', style={'margin-top': '40px', 'margin-bottom': '25px'}),
            dbc.CardBody(
                    [
                        dbc.Row([
                         dbc.Col(
                        [
                            dbc.Card(children = [
                                dcc.Graph(
                                    id="asset_graph", 
                                    figure = balance_asset_structure_graph,
                                        )],
                                    style={"padding-top": "20px"}
                                      ),
                        ],
                    ),
                    dbc.Col(
                        dbc.Card([
                           dcc.Graph(id="capital_graph", figure = balance_passive_structure_graph),
                        ],
                        style={"padding-top": "20px"}
                        ),
                    )])],
                    ),


            html.H4('Отчет о финансовых результатах', style={'margin-top': '40px', 'margin-bottom': '25px'}),
            html.Div([
                            html.H5(['Вид диаграммы'], style={'margin-left': '20px', 'margin-right': '20px', 'margin-top': '20px'}),
                            dcc.RadioItems(
                                id='radio',
                                options=[
                                        {'label': html.Span("Линейная", style={'font-size': 20, 'padding-left': 6}), 'value': 'Линейная'},
                                        {'label':  html.Span("Гистограмма", style={'font-size': 20, 'padding-left': 6}), 'value': 'Гистограмма'},
                                ],
                                value='Линейная',
                                style={"font-size": "20px"},
                                labelStyle={"display": "flex", "align-items": "center"},
                                # inline = True
                            ),
                        ],
                        style={'display': 'flex',
                               'flex-direction': 'row',
                               'justify-content': 'left',
                               'margin-bottom': '25px'
                               }),
            dbc.Card([
                        #    dcc.Graph(id="result_analyse_graph", figure = ofr_line_graph),
                        
                        
                        
                        dcc.Graph(id='ofr_line_graph')
                       
                        ],
                        style={"padding-top": "20px"}
                        ),
            


            html.H4('Отчет о движении денежных средств', style={'margin-top': '40px', 'margin-bottom': '25px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id="odds_saldo", figure = odds_saldo_graph),
                    ]),
                ]),
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id="odds_postup", figure = odds_rises_graph),
                    ])
                ])
            ]),
            html.H4('', style={'margin-top': '40px', 'margin-bottom': '25px'}),
            

            

            
        ],
        
    )
