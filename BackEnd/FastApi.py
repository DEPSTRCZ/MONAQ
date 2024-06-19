from decimal import Decimal
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from models import Records
from DataBaseConnector import DataBaseConnector
from sqlmodel import SQLModel
from datetime import datetime
import pandas as pd




app = FastAPI()
db = DataBaseConnector()

# Type defs
class SensorResponse(SQLModel):
    sensor_id: int
    times_posted: int
    last_update: datetime
    records: list[Records]

class SimpleSensorResponse(SQLModel):
    temperature: Decimal
    updated_at: datetime
    sensor_id: int
    co2: int
    humidity: Decimal
    loc_lat: Decimal
    loc_long: Decimal
class GetAllSensorsResponse(SQLModel):
    count: int
    sensors: list[SimpleSensorResponse]

class GetQualityInfo(BaseModel):
    humidity: Decimal
    temperature: Decimal
    co2: int
    delta_co2: int
    delta_humidity: Decimal
    delta_temperature: Decimal


@app.get("/getAllSensors",response_model=GetAllSensorsResponse)
def read_sensors(limitRecords: Union[int, None] = None):
    """
    Returns all sensors in the database in a json format along with their latest metrics. All dates are in UTC.
    """
    results = db.GetSensors(limitRecords)
    response = dict()
    response["count"] = len(results)
    response["sensors"] = results
    return response


@app.get("/getSensor/{sensor_id}",response_model=SensorResponse)
def read_sensors(sensor_id: int, limit: Union[int, None] = None):
    """
    Return sensor by id {sensor_id} in a json format. Along with all their records. All dates are in UTC.
    [Warning] If no limit is provided the browser might crash. :D
    """
    sensor = db.GetSensor(sensor_id, limit)

    return sensor

@app.get("/getQualityInfo/{sensor_id}",response_model=GetQualityInfo)
def get_quality_info(sensor_id: int):
    """
    Returns quality info for the latest 2 records for the sensor with id {sensor_id}
    This endpoint was made quickly and might not be most accurate. Probably needs some refactor..
    """


    # Get latest 2 records
    sensors = db.GetSensor(sensor_id, limit=2)
    response = dict()

    # Create dataframe
    records_list = [record.__dict__ for record in sensors.records]
    
    # Remove the '_sa_instance_state' key which is added by SQLAlchemy
    for record_dict in records_list:
        record_dict.pop('_sa_instance_state', None)
    
    # Create the DataFrame
    df = pd.DataFrame(records_list)
    
    df[["humidity", "loc_lat", "loc_long", "temperature",]] = df[["humidity", "loc_lat", "loc_long", "temperature",]].astype(float)
    df = df.sort_values(by="updated_at", ascending=False)

    # Get latest 2 records
    df_delta = df.head(2)
    df_delta["delta_humidity"] = df_delta["humidity"].diff()
    df_delta["delta_temperature"] = df_delta["temperature"].diff()
    df_delta["delta_co2"] = df_delta["co2"].diff()

    # Asign deltas and values for each metric.
    response["delta_humidity"] = round(df_delta['humidity'].iloc[-1] - df_delta['humidity'].shift(1).iloc[-1],2)
    response["delta_temperature"] = round(df_delta['temperature'].iloc[-1] - df_delta['temperature'].shift(1).iloc[-1],2)
    response["delta_co2"] = df_delta['co2'].iloc[-1] - df_delta['co2'].shift(1).iloc[-1]
    response["humidity"] = df_delta.iloc[-1]['humidity']
    response["temperature"] = df_delta.iloc[-1]['temperature']
    response["co2"] = df_delta.iloc[-1]['co2']

    return response