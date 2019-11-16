import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from utils_app import *
from app import *
import json


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config['suppress_callback_exceptions']=True
app.scripts.config.serve_locally=True

#########################################################


########################################################
# General layout for all the pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar(),
    html.Div(id='page-content')
])

drop_opts1 = [dict(label=d[0], value=d[0]) for d in list(zip(metadata['description'], metadata['group'])) if d[1] == 'default']
drop_opts2 = [dict(label=d[0], value=d[0]) for d in list(zip(metadata['description'], metadata['group'])) if d[1] != 'default']
range = range_slider('range', [12, 16])
# knob = daq_knob('knob', 0)
# datepicker = datepicker('datepicker')
# toggle1 = daq_toggle('toggle', value=True, label=['lines', 'points'])
# print(metadata[metadata['description']=='Amos Rex']['latitude'].values)
# print(metadata[metadata['description']=='Amos Rex']['longitude'].values)

dropdownSt = dash_dropdown(
    'other-st',
    'Amos Rex',drop_opts1,
    pd_top=0, pd_bottom=0,
    pd_right=0, pd_left=0
)

dropdownH = dash_dropdown(
    'harbor-st',
    'Hernesaari LHC',drop_opts2,
    pd_top=5, pd_bottom=0,
    pd_right=0, pd_left=0
)

map = dash_graph('map', height='88vh', scrollZoom=True)
row_args = (
    card('options-card', 3, dropdownH, dropdownSt, range, height='92vh'),
    card('map-card', 9, map),
)

index_layout = html.Div([
    row(*row_args)
])

lons = pd.unique(metadata['longitude'])
lats = pd.unique(metadata['latitude'])
#################################################
# Callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_layout
    else:
        return '404'


@app.callback(Output('map', 'figure'),
              [Input('other-st', 'value'),
               Input('harbor-st','value'),
               Input('range', 'value')])
def render_on(drop1, drop2, range):
    lon1 = metadata[metadata['description']==drop2]['longitude'].values
    lon2 = metadata[metadata['description']==drop1]['longitude'].values
    lat1 = metadata[metadata['description']==drop2]['latitude'].values
    lat2 = metadata[metadata['description']==drop1]['latitude'].values
    t1 = metadata[metadata['description']==drop1]['description'].values
    t2 = metadata[metadata['description']==drop2]['description'].values
    txt = '{} - {}'.format(t2[0], t1[0])
    return scatterMap(
        longitudes=lons,
        latitudes=lats,
        lineLon=[lon1[0], lon2[0]],
        lineLat=[lat1[0], lat2[0]],
        linename=txt
    )


@app.callback(
    Output('range-output', 'children'),
    [Input('range', 'value')])
def update_output(value):
    return 'time: {}.00 - {}.00'.format(value[0], value[1])

#################################################
# Run app
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
