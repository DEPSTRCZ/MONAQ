from typing import Union
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime
from models import Sensors,Records
from DataBaseConnector import DataBaseConnector
from fastapi import FastAPI




app = FastAPI()
db = DataBaseConnector()


class GetAllSensorsResponse(BaseModel):
    count: int
    results: list[Sensors]
# Type defs
class SensorResponse(SQLModel):
    sensor_id: int
    times_posted: int
    last_update: datetime
    records: list[Records]


@app.get("/")
def read_root():
    return {}


@app.get("/getAllSensors",response_model=GetAllSensorsResponse)
def read_sensors():
    """
    Returns all sensors in the database in a json format.
    """
    response = dict()
    results = db.GetSensors()
    response["count"] = len(results)
    response["results"] = results

    return response


@app.get("/getSensor/{sensor_id}",response_model=SensorResponse)
def read_sensors(sensor_id: int):
    """
    Return sensor by id {sensor_id} in a json format.
    """
    sensor = db.GetSensor(sensor_id)
    return sensor
