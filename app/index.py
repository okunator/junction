import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
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

drag_drop = drag_drop('drag-drop')
drop_opts1 = [dict(label=d[0], value=d[0]) for d in list(zip(metadata['description'], metadata['group'])) if d[1] == 'default']
drop_opts2 = [dict(label=d[0], value=d[0]) for d in list(zip(metadata['description'], metadata['group'])) if d[1] != 'default']
range = range_slider('range', [12, 16])
toggle = daq_toggle('toggle', value=False, label=['did not return','returned to port'])

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
countplotp = dash_graph('countplot-g', height='40vh', loading=True, loading_num=1)

row_args = (
    card('options-card', 3, drag_drop, dropdownH, dropdownSt, toggle, range, countplotp, height='92vh'),
    card('map-card', 9, map),
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


@app.callback(Output('countplot-g', 'figure'),
              [Input('other-st', 'value'),
               Input('harbor-st','value'),
               Input('range', 'value'),
               Input('toggle', 'value')])
def counts(drop1, drop2, range1, toggle):
    data1 = df[df['description'] == drop2]
    data2 = df[df['description'] == drop1]
    data_in = pd.merge(data1, data2, how='inner', on=['hashes'])
    data1 = df[df['description'] == drop2]
    data2 = df[df['description'] != drop1]
    data_out = data2[~data2['hashes'].isin(data_in['hashes'])]
    # if toggle:
    #     data1 = data1[data1['returned']==1]
    #     data2 = data1[data1['returned']==1]
    # else:
    #     data1 = data1[data1['return']==0]
    #     data2 = data1[data1['return']==0]

    print(df.shape)

    # data1 = df[df['hour'].between(range1[0], range1[1)]
    # data2 = df[df['hour'].between(range1[0], range1[1)]
    data_counts1 = data_in.shape[0]
    data_counts2 = data_out.shape[0]
    print(data_counts2-data_counts1)
    count_df = pd.DataFrame({'yes':[data_counts1], 'no':[data_counts2]})

    return countplot(count_df)


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


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#################################################
# Run app
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
