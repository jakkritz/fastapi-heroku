from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "https://fastapi-prototyping.herokuapp.com/docs"}


@app.post('/dialogflow/fulfillment/payment')
def dialogflow_scb_payment(request):
    return {k: v for k, v in request}
