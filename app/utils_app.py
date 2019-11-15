import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from textwrap import dedent as d

################################################################################
################################################################################
################## FUNCTION WRAPPERS FOR LAYOUT MANAGEMENT #####################
################################################################################
################################################################################
def navbar():
    """Create the app navbar with dash bootstrap navbar"""
    return dbc.Navbar([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Flow app", className="ml-2"))
                    ],
                    align="center",
                    no_gutters=True
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
        ],
        color="blue",
        dark=True,
        className='mx-auto navbar-nav navbar-expand-lgpx-12'
    )


def nav_menu():
    """Create the app nav-tab with dash Tabs object"""
    return html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Overview', value='tab-1'),
            dcc.Tab(label='Sample set summary', value='tab-2'),
            dcc.Tab(label='Dimensionality reduction', value='tab-3'),
            dcc.Tab(label='Unsupervised clustering', value='tab-4'),
            dcc.Tab(label='Populations trees', value='tab-5'),
        ], colors={"border": "#d1e3ff", "primary": "#1a7ef0", "background": "#d9d9d9"}
        ),
        html.Div(id='tabs-content')
    ])


def app_layout():
    """Create the parent <div> of the app where all of the contents are rendered"""
    return html.Div([
        dcc.Location(id='url', refresh=False),
        navbar(),
        html.Div(id='page-content'),
        nav_menu()
    ])


def row(*args):
    """Bootstrap row dash wrapper"""
    return html.Div([
        html.Div(args, className='row')
    ], style={'padding-top': 5, 'padding-left': 15, 'padding-right': 15})


def card_column(*args) :
    """Bootstrap card column (3-column grid) wrapper"""
    return html.Div(args, className='card-columns pt-2')


def card(id, grid_num=12, comp1=None, comp2=None, comp3=None, comp4=None, comp5=None, comp6=None,
          comp7=None, comp8=None, comp9=None, comp10=None, comp11=None, comp12=None, comp13=None, height=None):
    """Bootstrap card dash wrapper"""
    return html.Div([
                html.Div([
                    html.Div([
                        comp1,
                        comp2,
                        comp3,
                        comp4,
                        comp5,
                        comp6,
                        comp7,
                        comp8,
                        comp9,
                        comp10,
                        comp11,
                        comp12,
                        comp13
                    ], className='p-1 card-body', id=id, style={"height": height})
                ], className='card shadow p-1')
            ], className='pl-1 pr-1 col-sm-{} col-md-{} col-lg-{}'.format(grid_num, grid_num, grid_num))


def column(id, grid_num=12, comp1=None, comp2=None, comp3=None, comp4=None, comp5=None,comp6=None,
         comp7=None, comp8=None, comp9=None, comp10=None, comp11=None, comp12=None, comp13=None):
        """Simple bootstrap column function wrapper"""
        return html.Div([
                    html.Div([
                        comp1,
                        comp2,
                        comp3,
                        comp4,
                        comp5,
                        comp6,
                        comp7,
                        comp8,
                        comp9,
                        comp10,
                        comp11,
                        comp12,
                        comp13
                    ], className='p-1 text-center', id=id)
                ], className='p-1 col-sm-{} col-md-{} col-lg-{}'.format(grid_num, grid_num, grid_num))


def info_card(text1=None, text2=None, text3=None, text4=None,
              colwidth1=3, colwidth2=3, colwidth3=3, colwidth4=3,
              comp1=None, comp2=None, comp3=None, comp4=None):
    """A bootstrap card with title and text as content"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P(text1, className='mb-1'),
                    comp1
                ], width=colwidth1, className='px-1'),
                dbc.Col([
                    html.P(text2, className='mb-1'),
                    comp2
                ], width=colwidth2, className='px-1'),
                dbc.Col([
                    html.P(text3, className='mb-1'),
                    comp3
                ], width=colwidth3, className='px-1'),
                dbc.Col([
                    html.P(text4, className='mb-1'),
                    comp4
                ], width=colwidth4, className='px-1')
            ])
        ], className='pt-1 pb-1')
    ], className='text-center')
################################################################################
################################################################################
####################### FUNCTION WRAPPERS FOR WIDGETS ##########################
################################################################################
################################################################################

def accordion_item(*args, **kwargs):
    """Creates an item in the accordion"""
    return html.Div([
        dbc.Card(
        [
            html.Div([
                dbc.CardHeader(
                    html.H2(
                        dbc.Button(
                            "{}".format(kwargs['name']),
                            color="link",
                            id="group-{}-toggle".format(kwargs['i']),
                        )
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(
                        html.Div([
                            *args
                        ])
                    ),
                    id="collapse-{}".format(kwargs['i']),
                )
            ])
        ]
    )])


def create_accordion(*args, **kwargs):
    """Creates a collapsible bootstrap accordion"""
    return html.Div(
        html.Div([
            *args
        ],className="accordion")
    )


def dbc_dropdown(id, options=[{'label':'Dummy', 'value':'Dummy'}],
                multi=False, pd_top=2.5, pd_bottom=2.5):

    children = [dbc.DropdownMenuItem(d['value'], id="dropdown-{}-item".format(d['value'])) for d in options]
    dropdown = dbc.DropdownMenu(
        label="Central values",
        children=children
    )
    return dropdown


def dbc_buttongroup(options, size="md", vertical=False):
    """dash bootstrap components function wrapper for buttongroup"""
    # First button is set as active
    buttons=[]
    for i, d in enumerate(options):
        if i == 0:
            buttons.append(dbc.Button(d, id="button-{}".format(d), className="btn active", n_clicks=1))
        else:
            buttons.append(dbc.Button(d, id="button-{}".format(d), className="btn"))

    return html.Div([
        dbc.ButtonGroup(buttons, size=size, vertical=vertical)
    ])


def dash_pre(id, height=40):
    """html <pre> dash object wrapper"""
    return html.Div([
        html.Pre(
            id=id,
            style={
                'border':'thin lightgrey solid',
                'height':height,
                'padding-top': 15,
                'padding-left': 30,
                'padding-right': 30
            }
        )
    ], style={'padding-top':15})


def daq_toggle(id, value, label, margin_left=0, margin_right=0, disabled=False):
    """DAQ toggle switch wrappers"""
    return html.Div([
        daq.ToggleSwitch(
            id=id,
            size=30,
            value=value,
            theme=dict(primary=True),
            label=label,
            disabled=disabled,
            style={
                'padding':5,
                'margin-left':margin_left,
                'margin-right':margin_right
            }
        )
    ])

def dash_dropdown(id, value, options=[{'label':'Dummy', 'value':'Dummy'}],
                  multi=False, pd_top=2.5, pd_bottom=2.5, pd_right=30, pd_left=30):
    """Dash dropdown object wrapper"""
    return html.Div([
        dcc.Dropdown(
            id=id,
            options=options,
            value=value,
            clearable=False,
            multi=multi
        )
    ], style={
            'padding-top': pd_top,
            'padding-bottom':pd_bottom,
            'padding-left': pd_left,
            'padding-right': pd_right
        }
    )


def dash_radiobuttons(id, value, options=[{'label': 'Dummy', 'value': 'Dummy'}]):
    """Dash radiobuttons object wrapper"""
    return html.Div([
            dcc.RadioItems(
                id=id,
                options=options,
                value=value,
                labelStyle={'display': 'inline-block', 'padding-left':4, 'padding-right':4}
            )
        ], style={
            'padding-top':2.5,
            'padding-bottom':0,
            'padding-left':30,
            'padding-right':30
        }
    )


def dash_table_wrap(id, row_select=False, df=None):
    """Dash data table object wrapper"""
    if df is not None:
        return dash_table.DataTable(
            id=id,
            data=df.to_dict("rows"),
            columns=[{"name": i, "id": i} for i in df.columns],

            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold',
                'color': 'white',
                'textAlign': 'left'
            },
            style_cell={
                'color': 'rgb(70, 70, 70)',
                'textAlign': 'left',
                'padding':'8px'
            },

            fixed_rows={'headers': True, 'data': 0},

            style_table={
                'overflowY': 'scroll'
            }
        )
    else:
        return dash_table.DataTable(
            id=id,
            data=pd.DataFrame().to_dict('rows'),

            style_header={
                'fontWeight': 'bold',
                'textAlign': 'left',
                'padding':'8px'
            },
            style_cell={
                'color': 'rgb(70, 70, 70)',
                'textAlign': 'left',
                'padding':'8px',
                'minWidth':'115px'
            },

            fixed_rows={'headers': True, 'data': 0},

            style_table={
                'overflowY': 'scroll',
                'overflowX': 'scroll'
            }
        )

################################################################################
################################################################################
######## FUNCTION WRAPPERS FOR DASH TABLE OBJS AND PLOTLY GRAPH OBJS ###########
################################################################################
################################################################################

def dash_table_paginate(id, height, width, row_select=False, data=[], columns=[]):
    """Dash data table object wrapper"""
    return dash_table.DataTable(
        id=id,
        data=data,
        columns=columns,

        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'left'
        },
        style_cell={
            'color': 'rgb(70, 70, 70)',
            'textAlign': 'left',
            'minWidth': '140px', 'maxWidth': '280px',
            'padding':'8px'
        },

        fixed_rows={'headers': True, 'data': 0},

        style_table={
            'overflowY':'scroll',
            'overflowX':'scroll'
        },

        page_current=0,
        page_size=8,
        page_action='native'
    )


def dash_graph(id, figure=None, height=None, scrollZoom=False, loading=False, loading_num=0):
    """Dash graph object wrapper"""
    if figure != None:
        return dcc.Graph(
            id=id,
            figure=figure,
            style={"height": height},
            config={'displaylogo':False, 'scrollZoom':scrollZoom, 'autosizable':True}
        )
    elif loading and loading_num != 0:
        return dcc.Loading(
            id="loading-{}".format(loading_num),
            children=[
                dcc.Graph(
                    id=id,
                    figure=go.Figure(
                        layout=go.Layout(
                            plot_bgcolor='rgb(255,255,255)',
                            yaxis=dict(
                                mirror= False,
                                showgrid=False,
                                showline=False,
                                zeroline=False,
                                showticklabels=False,
                                ticks=""
                            ),
                            xaxis=dict(
                                mirror= False,
                                showgrid=False,
                                showline=False,
                                zeroline=False,
                                showticklabels=False,
                                ticks=""
                            )
                        )
                    ),
                    config={
                        'displaylogo':False,
                        'scrollZoom':scrollZoom,
                        'autosizable':True,
                    },
                    style={"height": height},
                )
            ],
            type="circle",
            style={
                'height':height,
                'display':'flex',
                'align-items':'center'
            }
        )
    else:
        return dcc.Graph(
            id=id,
            figure=go.Figure(
                layout=go.Layout(
                    plot_bgcolor='rgb(255,255,255)',
                    yaxis=dict(
                        mirror= False,
                        showgrid=False,
                        showline=False,
                        zeroline=False,
                        showticklabels=False,
                        ticks=""
                    ),
                    xaxis=dict(
                        mirror= False,
                        showgrid=False,
                        showline=False,
                        zeroline=False,
                        showticklabels=False,
                        ticks=""
                    )
                )
            ),
            config={
                'displaylogo':False,
                'scrollZoom':scrollZoom,
                'autosizable':True,
                'displayModeBar': False
            },
            style={"height": height},
        )


def dash_markdown(text):
    """Dash markdown object wrapper"""
    return html.Div([
        dcc.Markdown(d("""{}""".format(text)))
    ], style={'padding-top': 10, 'padding-left': 15, 'padding-right': 15})


def dash_store(id, storage_type='memory'):
    return dcc.Store(id, storage_type)
