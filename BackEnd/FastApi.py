from typing import Union
from fastapi import FastAPI
from models import Sensors,Records
from DataBaseConnector import DataBaseConnector
from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime




app = FastAPI()
db = DataBaseConnector()




# Type defs
class SensorResponse(SQLModel):
    sensor_id: int
    times_posted: int
    last_update: datetime
    records: list[Records]

class GetAllSensorsResponse(SQLModel):
    count: int
    sensors: list[SensorResponse]

@app.get("/getAllSensors",response_model=GetAllSensorsResponse)
def read_sensors():
    """
    Returns all sensors in the database in a json format.
    """
    results = db.GetSensors()
    response = dict()
    response["count"] = len(results)
    response["sensors"] = results
    return response


@app.get("/getSensor/{sensor_id}",response_model=SensorResponse)
def read_sensors(sensor_id: int):
    """
    Return sensor by id {sensor_id} in a json format.
    """
    sensor = db.GetSensor(sensor_id)

    return sensor
