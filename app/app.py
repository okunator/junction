import dash
import pickle
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from utils_app import *
import deckglplotly

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config['suppress_callback_exceptions']=True
app.scripts.config.serve_locally=True

#########################################################
json = [{"sourcePosition": [-56.256744, -34.8749], "targetPosition": [-56.255649, -34.874753], "color": [96, 41, 243, 203], "width": 2, "legend_title": "TEST", "legend_data": 23}]
deck = deckglplotly.LineLayer(
            id='map',
            longitude=-56.256744,
            latitude=-34.8749,
            zoom=16,
            data=json[0],
            mapboxtoken='pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg',
        )
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

row_args = (
    card('options-card', 2, dropdown1, dropdown2, height='92vh'),
    card('map-card', 10, deck, height='92vh'),
)

index_layout = html.Div([
    row(*row_args)
])


#################################################
# Callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_layout
    else:
        return '404'

#################################################
# Run app
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
