from typing import Union
from fastapi import FastAPI
from tortoise.models import Model
from tortoise import fields, Tortoise
import asyncio

app = FastAPI()


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='mysql://moniaq:admin@localhost:3306/moniaq',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

asyncio.run(init())


@app.get("/")
def read_root():
    return {}


@app.get("/getSensors/{sensor_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}