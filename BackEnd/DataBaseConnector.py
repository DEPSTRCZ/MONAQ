from sqlmodel import Field, SQLModel, create_engine, Session, select
from models import Records,Sensors
from datetime import datetime
import os
from sqlalchemy.orm import selectinload




DATABASE_URL = os.getenv("DATABASE_URL")




class DataBaseConnector():
    def __init__(self) -> None:
        # Establishing a connection to the MySQL database
        self.engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(self.engine)


    def SaveRecord(self, data):
        with Session(self.engine) as session:
            # Check if sensor already exists
            result = session.exec(select(Sensors).where(Sensors.sensor_id == data["id"])).first()

            # If not, create new sensor
            if not result:
                sensor = Sensors(sensor_id=data["id"], times_posted=1, last_update=datetime.now())
                session.add(sensor)
            else:
                # If yes, update sensor
                sensor = result
                sensor.times_posted += 1
                sensor.last_update = datetime.now()
                session.add(sensor)

            # Save record & commit
            record = Records(
                sensor_id=sensor.sensor_id,
                co2=data["co2"], 
                temperature=data["temperature"],
                humidity=data["humidity"], 
                loc_lat=data["loc_lat"], 
                loc_long=data["loc_long"]
            )

            session.add(record)
            session.commit()
    
    # Get all sensors from database
    def GetSensors(self):
        with Session(self.engine) as session:
            result = session.exec(
                        select(Sensors).options(selectinload(Sensors.records))
                    ).all()

            return result
        

    def GetLatestRecordFromList(self,records):
        ## Returns the latest record from a list of records by "last_update"
        return max(records, key=lambda record: record.updated_at)
        
        

    # Get sensor from database
    def GetSensor(self, sensor_id):
        with Session(self.engine) as session:
            result = session.exec(select(Sensors).where(Sensors.sensor_id == sensor_id)).first()
            # Sort the records by data
            #sort_by_date = sorted(result.records,key=lambda x: x.updated_at,reverse=True)
            # Asing the sorted
            #result.records = sort_by_date[:1]
            result.records
            return result

        
