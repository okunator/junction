import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import os
import numpy as np
import pandas as pd
import requests
import plotly.graph_objs as go
import plotly.figure_factory as ff
from textwrap import dedent as d
from datetime import datetime as dt
from app import *

################################################################################
################################################################################
################## FUNCTION WRAPPERS FOR LAYOUT MANAGEMENT #####################
################################################################################
################################################################################
mapbox_access_token = 'pk.eyJ1IjoidGhlcmVhbGhhY2tlciIsImEiOiJjazMwcGE5dmQwMHF2M2NtamZ1MDdveHJpIn0.ELMe25hitkC1JlgNdFeCSg'

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
                    ], className='card-body', id=id, style={"height": height})
                ], className='card shadow')
            ], className='col-sm-{} col-md-{} col-lg-{}'.format(grid_num, grid_num, grid_num))


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


################################################################################
################################################################################
####################### FUNCTION WRAPPERS FOR WIDGETS ##########################
################################################################################
################################################################################

def daq_knob(id, value, margin_left=0, margin_right=0):
    """DAQ knob"""
    return html.Div([
        daq.Knob(
            label="Time",
            id=id,
            max=24,
            value=1,
            min=1,
            scale={'start':1, 'labelInterval': 1, 'interval': 1}
        ),
        html.Div(id='knob-output', className='px-3 pt-4')
    ], className='px-5 pt-4')


def datepicker(id):
    return html.Div([
        dcc.DatePickerSingle(
            id=id,
            min_date_allowed=dt(2019, 8, 5),
            max_date_allowed=dt(2020, 9, 19),
            initial_visible_month=dt(2019, 8, 5),
            date=str(dt(2019, 8, 25, 23, 59, 59))
        ),
        html.Div(id='output-container-date-picker-single')
    ], className='px-5 pt-5 pd-5 mx-3')


def range_slider(id, value):
    return html.Div([
        dcc.RangeSlider(
            id=id,
            marks={i: '{}'.format(i) for i in range(1, 24)},
            min=1,
            max=24,
            value=value
        ),
        dash_pre(id='pre', html.Div(id='range-output', className='pt-5 px-7 pd-4'))
    ], className='px-2 pt-4 pd-4')



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
                'padding':5
            }
        )
    ], className='pt-4 px-5')


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
        },
        className='pt-4'
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


def scatterMap(longitudes=None, latitudes=None, lineLon=None, lineLat=None, linename=None):
    data = []
    for i, (lon, lat) in enumerate(list(zip(longitudes, latitudes))):
        data.append(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            name=metadata['description'][i],
            hovertext=['{}<br>{}'.format(metadata['description'][i], metadata['address'][i])],
            hoverinfo='lon+lat+text',
            marker=dict(size=12)
        ))

    line = go.Scattermapbox(
        lat=lineLat,
        lon=lineLon,
        mode='markers+lines',
        hovertext=linename,
        name=linename,
        hoverinfo='text'
    )
    data.append(line)

    fig = go.Figure(data)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lon=24.9442,
                lat=60.16531
            ),
            pitch=0,
            zoom=12,
        ),
    )
    fig.update_layout(mapbox_style='dark')
    return fig
