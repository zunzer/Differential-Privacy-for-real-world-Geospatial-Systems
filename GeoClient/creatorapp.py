import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import scipy.ndimage as ndimage
from dash import dcc, html
from dash.dependencies import Input, Output, State
from postgres import execute_query


def creator_layout():
    layout = dbc.Container(
        [
            html.Br(),
            html.Div(
                [
                    html.Label("Latitude: "),
                    dcc.Input(
                        id="latitude-input",
                        type="number",
                        value=None,
                        style={"width": "100%"},
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                [
                    html.Label("Longitude: "),
                    dcc.Input(
                        id="longitude-input",
                        type="number",
                        value=None,
                        style={"width": "100%"},
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                [
                    html.Label("Income: "),
                    dcc.Dropdown(
                        id="income",
                        options=[
                            {"label": "10001 to 25000", "value": "10001 to 25000"},
                            {"label": "25001 to 50000", "value": "25001 to 50000"},
                            {"label": "More than 50000", "value": "More than 50000"},
                            {"label": "Below Rs.10000", "value": "Below Rs.10000"},
                            {"label": "No Income", "value": "No Income"},
                        ],
                        value="",
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                [
                    dcc.Loading(
                        id="loading2",
                        type="circle",
                        children=[
                            html.Button(
                                "Add Datapoint",
                                id="submit-query",
                                n_clicks=0,
                                style={
                                    "align": "center",
                                    "width": "100%",
                                    "height": "1cm",
                                    "display": "inline-block",
                                    "background-color": "#0e1012",
                                    "border": "none",
                                    "color": "white",
                                },
                            ),
                            html.Div(id="output-submit"),
                        ],
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.Div(
                [
                    dcc.Loading(
                        id="loading21",
                        type="circle",
                        children=[
                            html.Button(
                                "Delete all added Datapoints",
                                id="delete-query",
                                n_clicks=0,
                                style={
                                    "align": "center",
                                    "width": "100%",
                                    "height": "1cm",
                                    "display": "inline-block",
                                    "background-color": "#0e1012",
                                    "border": "none",
                                    "color": "white",
                                },
                            ),
                            html.Div(id="output-delete"),
                        ],
                    )
                ]
            ),
        ],
        style={"width": "100%"},
    )
    return layout


# Callback to update the values of the figure


def creator_callbacks(app):
    @app.callback(
        Output("output-submit", "children"),
        [
            State("longitude-input", "value"),
            State("latitude-input", "value"),
            State("income", "value"),
        ],
        Input("submit-query", "n_clicks"),
    )
    def display_value(long, lat, income, nclicks):
        if nclicks > 0:
            print("Execute insert")
            _ = execute_query(
                "INSERT INTO online_delivery_data VALUES (388, 20, 'Female', 'Married', 'Student','"
                + str(income)
                + "', 'Post Graduate', 3, 560001, 'Food delivery apps', 'Web browser', 'Breakfast', 'Lunch', 'Non Veg foods (Lunch / Dinner)', 'Bakery items (snacks)', 'Neutral',	'Neutral',	'Neutral',	'Neutral',	'Neutral', 'Neutral', 'Neutral', 'Neutral',	'Neutral', 'Neutral', 'Neutral', 'Neutral', 'Neutral', 'Neutral', 'Agree', 'Agree',	'Agree', 'Agree', 'Agree', 'Agree',	'Yes', 'Weekend (Sat & Sun)', '30 minutes', 'Agree', 'Neutral', 'Neutral', 'Neutral', 'Neutral', 'Yes', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Moderately Important', 'Yes', 'TEST ENTRY', ST_GeometryFromText('POINT (65.9901232886963 55.5953903123242)', 4326));"
            )  # ST_GeometryFromText('POINT (" +str(long) + " " + str(lat) +")', 4326));")
            print("Executed insert")
            return f"Value: {long},{lat},{income}, {nclicks}"
        else:
            return

    @app.callback(
        Output("output-delete", "children"), Input("delete-query", "n_clicks")
    )
    def display_value(nclicks):
        if nclicks > 0:
            print("Execute delete")
            _ = execute_query(
                'DELETE FROM public.online_delivery_data WHERE "index"=388'
            )
            print("Finished delete")
            return f"Value: {0}"
        else:
            return
