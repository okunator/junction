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

drop_opts = [dict(label='Dummy', value='Dummy')]

dropdown1 = dash_dropdown(
    'mst-dropdown-marker',
    'Dummy',drop_opts,
    pd_top=0, pd_bottom=0,
    pd_right=0, pd_left=0
)

dropdown2 = dash_dropdown(
    'mst-dropdown-marker',
    'Dummy',drop_opts,
    pd_top=5, pd_bottom=0,
    pd_right=0, pd_left=0
)

toggle1 = daq_toggle('toggle', value=True, label=['off', 'on'])

map = dash_graph('map', height='88vh', scrollZoom=True)


row_args = (
    card('options-card', 2, dropdown1, dropdown2, toggle1, height='92vh'),
    card('map-card', 10, map),
)

index_layout = html.Div([
    row(*row_args)
])

print(df.head())
print(len(df))
print(len(pd.unique(df['longitude'])))
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
              [Input('toggle', 'value')])
def render_lines(value):
    if value:
        return scatterMap(
            longitudes=df['longitude'],
            latitudes=df['latitude'],
            mapbox_style='dark',
            show=value
        )
    else:
        return scatterMap(mapbox_style="dark", show=value)

#################################################
# Run app
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
