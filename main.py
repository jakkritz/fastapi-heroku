from fastapi import FastAPI, APIRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel

import dash 
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

import pandas as pd


class Link(BaseModel):
    title: str
    url: str


# Create the Dash application, make sure to adjust requests_pathname_prefix
app_dash = dash.Dash(__name__, requests_pathname_prefix='/dash/')
app_dash.layout = html.Div(children=[
    html.H1(children='SuperAI: Supermarket Dashboard'),
    html.H5(children='''
        แดชบอร์ดข้อมูลซุปเปอร์มาร์เก็ต (โครงการซุปเปอร์เอไอเอนจิเนียร์)
    '''),
    html.P(children='''
        22p24i0146: จักรกฤษณ์
    '''),
    dcc.Graph(id='SpendTimeGraph'),
    html.Label([
        "Color Theme",
        dcc.Dropdown(
            id='colorScale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ])
    ]),
])


# Define callback to update graph
@app_dash.callback(
    Output('SpendTimeGraph', 'figure'),
    [Input("colorScale-dropdown", "value")]
)
def update_figure(colorScale):
    df = pd.read_csv('data/supermarket_for_app.csv')
    return px.scatter(
        df, x="SHOP_DATE", y="SPEND", color="QUANTITY",
        color_continuous_scale=colorScale,
        render_mode="webgl", title="Spend Over Time")


app = FastAPI()


@app.get("/")
def read_root():
    link_list: Links = [{'title': "api-test-routes",
                         'url': "https://fastapi-prototyping.herokuapp.com/docs"},
                        {'title': 'supermarket-dashboard',
                         'url': 'https://fastapi-prototyping.herokuapp.com/dash'},
                        {'title': 'other machine learning endpoints',
                         'url': 'https://ppsmartbot.com/docs'},
                        {'title': 'vue frontend for machine learning apps',
                         'url': 'https://ppsmartbot.com/login'}]
    return JSONResponse(content=jsonable_encoder(link_list))


@app.post('/dialogflow/fulfillment/payment')
def dialogflow_scb_payment(request):
    return {k: v for k, v in request}


# Now mount you dash server into main fastapi application
app.mount("/dash", WSGIMiddleware(app_dash.server))
