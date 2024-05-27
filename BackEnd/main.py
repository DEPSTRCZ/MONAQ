from typing import Union
import peewee
from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {}


@app.get("/getSensors/{sensor_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}