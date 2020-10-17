from fastapi import FastAPI, APIRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel

import dash 
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


class Link(BaseModel):
    title: str
    url: str
    description: Optional[str] = None


# Create the Dash application, make sure to adjust requests_pathname_prefx
app_dash = dash.Dash(__name__, requests_pathname_prefix='/dash/')
app_dash.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

app = FastAPI()


@app.get("/")
def read_root():
    link_list: Links = [{title: "api-test-routes", url: "https://fastapi-prototyping.herokuapp.com/docs"}]
    return JSONResponse(content=jsonable_encoder(link_list))


@app.post('/dialogflow/fulfillment/payment')
def dialogflow_scb_payment(request):
    return {k: v for k, v in request}


# Now mount you dash server into main fastapi application
app.mount("/dash", WSGIMiddleware(app_dash.server))
