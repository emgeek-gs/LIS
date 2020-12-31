import json
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import requests
import dash_core_components as dcc
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.title = 'Festus LIS'
#px.set_mapbox_access_token(open('.pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2tiaHNkcGgzMDhnNTJ5bHN0cnkycjA3ZyJ9.nWhzWvACygcA8P0bog-nOQ').read())
token = "pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg"

# Opening JSON file

response = requests.get('https://raw.githubusercontent.com/emgeek-gs/LIS/main/data/Parcel_Geo.geojson')
geoj = response.json()
# returns JSON object as
# a dictionary


df = pd.read_csv("https://raw.githubusercontent.com/emgeek-gs/LIS/main/data/LISFTS.csv")

size = df.iloc[:, 3]
size
fig = px.choropleth_mapbox(df, geojson=geoj, locations=df.id, featureidkey='properties.id', color="Size(Acres)",
                               color_continuous_scale="Rainbow",
                               range_color=(0, 270),
                               opacity=0.65,
                               hover_name="Parcel Number", hover_data=["Seller", "Size(Acres)", "Size(Hectares)","Location", "Map"])
fig.update_layout(title="Satellite View of Parcels")
fig.update_layout(mapbox_style='mapbox://styles/emmanuelnzyoka/ckiyknitw6tcx1al28jnkbqyk', mapbox_accesstoken=token,mapbox_zoom=11.7, mapbox_center = {"lat":-2.4448, "lon": 38.0991},margin={"r":0,"t":0,"l":0,"b":10})

fig.update_layout(title_font_size=30)
fig.update_traces(marker_line_color="white")
fig.update_traces(marker_line_width=2)
app.layout = html.Div([
html.H1("FESTUS MWANIKI LAND INFORMATION SYSTEM", style={'text-align': 'center','fontSize': 38}),
html.Div([
    html.Div(
                    [dcc.Graph(figure=fig, style={'maxHeight': '1500px'})],

                    ),
html.Div(
            [
                html.Div(
                    [
                        dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                fixed_rows={'headers': True},
                                style_cell={
                                        'textOverflow': 'ellipsis',
                                        'overflow': 'hidden',
                                        'textAlign': 'left',
                                        'padding': '5px'},
                                tooltip_delay=0,
                                tooltip_duration=None,

                                tooltip_data=[
                                     {
                                        column: {'value': str(value), 'type': 'markdown'}
                                         for column, value in row.items()
                                     } for row in df.to_dict('records')
                                 ],
                                data=df.to_dict('records'),
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto'
                                },

                                style_table={'maxHeight': '390px', 'overflowY': 'scroll'},
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'}],
                                style_header={
                                    'backgroundColor': 'rgb(128, 255, 0)',
                                    'fontWeight': 'bold'
                            },
                            ),
            ], style={'marginBottom': 50, 'marginTop': 25}, className="row"
        ),
    ])
    ])
    ],className='twelve columns div-for-charts bg-grey')

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
