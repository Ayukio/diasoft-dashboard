from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from bs4 import BeautifulSoup
import requests
from src.components.graphs_creator import kpi, kpi_col_names, balance_asset_structure, balance_asset_structure_col_names, balance_asset_structure_last_year, balance_passive_structure, balance_passive_structure_col_names, balance_passive_structure_last_year, ofr, odds_saldo, odds_saldo_col_names, odds_saldo_last_year, odds_rises, odds_rises_col_names, odds_rises_last_year
from src.components.data_extractor import YEARS

# THEME = px.colors.qualitative.Antique 
# THEME = px.colors.qualitative.Vivid_r 
# THEME = px.colors.qualitative.T10_r 

# THEME = [ '#46039f',  '#9c179e',  '#d8576b', '#fb9f3a', '#fdca26', '#f0f921']
THEME = [ '#2A2F4F',  '#E5BEEC',  '#917FB3', '#fb9f3a', '#fdca26', '#f0f921']
OFR_THEME = [ '#2A2F4F',  '#fb9f3a',  '#917FB3',  '#B3E5BE', '#D8576B']

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
                        'font': {'size': 46},
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

    kpis = {'Баланс': {'values': bal, 'y': float(f'{bal[-1]/(1000000):.3f}') , 'yo': float(f'{bal[-2]/(1000000):.3f}') , 'color': '#ffe8ce'},
        'Прибыль': {'values': prof, 'y': float(f'{prof[-1]/(1000000):.3f}') , 'yo': float(f'{prof[-2]/(1000000):.3f}') , 'color': '#ffe8ce'}, 
        'Выручка': {'values': rev, 'y': float(f'{rev[-1]/(1000000):.3f}') , 'yo': float(f'{rev[-2]/(1000000):.3f}') , 'color': '#ffe8ce'}, 
        'Капитал': {'values': tax, 'y': float(f'{tax[-1]/(1000000):.3f}') , 'yo': float(f'{tax[-2]/(1000000):.3f}') , 'color': '#ffe8ce'}}
    
    for _, (k, v) in enumerate(kpis.items()):
        if k == 'Баланс': fig_bal = get_kpi_plot(k, v) 
        if k == 'Прибыль': fig_prof = get_kpi_plot(k, v)
        if k == 'Выручка': fig_rev = get_kpi_plot(k, v)
        if k == 'Капитал': fig_tax = get_kpi_plot(k, v)

    year_options = []

    for k in YEARS:
       year_options.append({'label': k, 'value': k}) 



    long_df = px.data.medals_long()
    long_df.drop(long_df.tail(3).index,
            inplace = True)

    long_df.rename(columns={'nation': 'Вид операции', 'medal': 'Вид потока', 'count': 'Сумма'}, inplace=True)

    fig = px.histogram(long_df, x="Сумма",
                    y="Вид потока", color="Вид операции",
                    orientation='h',
                    barnorm='percent', text_auto='.2f',
                    # title="",
                    color_discrete_sequence=THEME,
                    ).update_layout(
                plot_bgcolor='#FFFFFF',
                margin=dict(l=0, r=0, b=0, t=15),
                legend_title = '',
                legend_x=-0.4, 
                legend_y=0.5,
                height=320,
                title={
                'text': "Структура операций",
                'y':0.9,
                'x':0.12,
                'xanchor': 'center',
                'yanchor': 'top'},
                font=dict(
                size=16,
            ),
            
        
    )


    
# ===========Разметка страницы===========

    return html.Div(
        className="app-div",
        style = {'margin': 'auto', 'width': '2100px', 'padding-top': '40px',
 
    },
        children=[
            dbc.Row(
            [
                dbc.Row(
                   [
                        html.Img(src=app.get_asset_url('diasoft-logo.png'),
                                 style={
                                    'height': '130%',
                                    'width': '19%',
                                    # 'font-size': 36,
                                    'padding-bottom': '50px'
                                }),
                        dcc.Graph(id='balance-indicator',
                                  figure = fig_bal,
                                style={
                                    'height': '95%',
                                    'width': '17%',
                                }),
                        dcc.Graph(id='profit-indicator',
                                  figure = fig_prof,
                                style={
                                    'height': '95%',
                                    'width': '17%',

                                }),
                        dcc.Graph(id='revenue-indicator',
                                  figure = fig_rev,
                                style={
                                    'height': '95%',
                                    'width': '17%',
                                }),
                        dcc.Graph(id='tax-indicator',
                                  figure = fig_tax,
                                style={
                                    'height': '95%',
                                    'width': '17%',
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

        html.Div(style = {'display': 'flex',
                        'flex-direction': 'row',
                        'justify-content': 'space-between',}, 
            children=[
                html.Div(style = {}, 
            children=[
html.H3('Бухгалтерский баланс', style={'margin-top': '40px', 'margin-bottom': '25px'}),
html.H3('', style={ 'margin-bottom': '40px'}),
            dcc.Dropdown(
                options = year_options, 
                value = 2022, 
                id='year-balance-dropdown', 
                style={ 'margin-bottom': '0px', 'width': '1305px', 'height': '32px', 'font-size': '18px'}
                         ),
            ]),
        
        html.Div(style = {}, 
            children=[
html.Div([
html.H3('Финансовые результаты', style={'margin-top': '0px', 'margin-bottom': '0px'}),
            html.Span([
                            # html.H5([''], style={'margin-left': '20px', 'margin-right': '0px', 'margin-top': '20px'}),
                            dcc.RadioItems(
                                id='radio',
                                options=[
                                        {'label': html.Span("Линейная", style={'font-size': 18, 'padding-left': 8, 'margin-right': 25}), 'value': 'Линейная'},
                                        {'label':  html.Span("Гистограмма", style={'font-size': 18, 'padding-left': 8}), 'value': 'Гистограмма'},
                                ],
                                value='Линейная',

                                style={"font-size": "20px"},
                                labelStyle={'display': 'inline-block'},
                                # inline = True
                            ),
                            
                        ],
                        style={'display': 'flex',
                               'flex-direction': 'row',
                               'justify-content': 'left',
                            #    'margin-bottom': '15px'
                               }),
            ],
            style={'display': 'flex',
                               'flex-direction': 'row',
                               'justify-content': 'space-between',
                               'align-items': 'center',
                               'margin-top': '40px',
                               'margin-bottom': '40px'
                               }
            ),               
            dcc.Dropdown(
                                id='ofr-category-selector',
                                options=list(ofr.columns[:-1]),
                                value=['Выручка', 'Чистая прибыль', 'Валовая прибыль'], 
                                multi=True,
                                style={ 'margin-top': '10px', 'margin-bottom': '10px', 'width': '770px'}
                            ),
        ]),           
            ]),

            
         
    
        html.Div(
            style = {'margin': 'auto', 'width': '900', 'padding-top': '0px',
    
        },
            children=[
            
            dbc.CardBody(
                    [
                        dbc.Row([
                         dbc.Col(
                        [
                            dbc.Card(children = [
                                dcc.Graph(
                                    id="asset_graph", 
                                        )],
                                    style={"padding-top": "0px"}
                                      ),
                        ],
                    ),
                    dbc.Col(
                        dbc.Card([
                           dcc.Graph(id="capital_graph", ),
                        ],
                        style={"padding-top": "0px"}
                        )),
                    dbc.Col(
                        # dbc.Card([
                          
            dbc.Card([
                      
                        dcc.Graph(id='ofr_line_graph')
                       
                        ],
                        
                        style={"padding-top": "0px", 'width': '770px', }
                        ),
                        # ],
                        style={"padding-top": "0px", }
                        
                    )])],
                    ),
                    # html.Div(
            # style = {'margin': 'auto', 'width': '800', 'padding-top': '0px',
    
        # })

            ]),


            
                        
            
            


            html.H3('Отчет о движении денежных средств', style={'margin-top': '40px', 'margin-bottom': '40px'}),
            dcc.Dropdown(
                options = year_options, 
                value = 2022, 
                id='year-odds-dropdown', 
                style={ 'margin-bottom': '15px'}
                         ),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id="odds_saldo"),
                    ], 
                    style={
                        'width': '630px'
                    }
                    ),
                ]),
                # dbc.Col([
                #     dbc.Card([
                #         dcc.Graph(id="odds_postup"),
                #     ])
                # ]),
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id="fig", figure=fig),
                    ], 
                    style={
                        'width': '1445px'
                    }
                    ),
                ]),
                dbc.Col([
                    html.Div([
                        # dcc.Graph(id="fig", figure=fig),
                    ], 
                    style={
                        'width': '1px'
                    }
                    ),
                ]),

            ]),
            html.H4('', style={'margin-top': '40px', 'margin-bottom': '25px'}),
            

            

            
        ],
        
    )
