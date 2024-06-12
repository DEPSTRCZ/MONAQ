from sqlmodel import Field, SQLModel, create_engine, Session, select
from models import Records,Sensors
from datetime import datetime
import os
from sqlalchemy.orm import selectinload
from sqlalchemy import func





DATABASE_URL = os.getenv("DATABASE_URL")




class DataBaseConnector():
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        This method establishes a connection to the MySQL database using the provided `DATABASE_URL`.
        It creates all the necessary tables and schema in the database using the `SQLModel.metadata.create_all()` method.

        Parameters:
            None

        Returns:
            None
        """
        # Establishing a connection to the MySQL database
        self.engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(self.engine)


    def SaveRecord(self, data):
        """
        Save a record to the database.

        This function takes a dictionary `data` containing information about a sensor and its associated records. 
        It checks if the sensor already exists in the database based on the sensor ID. If the sensor does not exist, 
        a new sensor is created with the provided sensor ID, and the number of times it has been posted is set to 1. 
        The last update time is set to the current datetime. If the sensor already exists, its `times_posted` attribute 
        is incremented by 1, and its `last_update` attribute is set to the current datetime.

        After determining the sensor, a new record is created with the provided sensor ID and the corresponding data values. 
        The record is then added to the session and the session is committed to save the changes to the database.

        Parameters:
            data (dict): A dictionary containing information about a sensor and its associated records.
                - sensor_id (int): The ID of the sensor.
                - co2 (float): The CO2 value of the record.
                - temperature (float): The temperature value of the record.
                - humidity (float): The humidity value of the record.
                - loc_lat (float): The latitude value of the record's location.
                - loc_long (float): The longitude value of the record's location.

        Returns:
            None
        """
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
    def GetSensors(self, limit=None):
        """
        Retrieves all sensors from the database along with their associated records.

        Returns:
            list: A list of Sensors objects, each containing information about a sensor and its associated records.
        """
        with Session(self.engine) as session:

            subquery = (
                select(Records.sensor_id, func.max(Records.updated_at).label("max_updated_at"))
                .group_by(Records.sensor_id)
                .subquery()
            )
            
            statement = (
                select(Records)
                .join(subquery, onclause=(Records.sensor_id == subquery.c.sensor_id) & 
                                    (Records.updated_at == subquery.c.max_updated_at))
            )
            
            results = session.exec(statement).all()

            return results
        

    # Get sensor from database
    def GetSensor(self, sensor_id, limit=None):
        """
        Retrieves a sensor from the database based on the provided sensor ID.

        Args:
            sensor_id (int): The ID of the sensor to retrieve.

        Returns:
            Sensors: The sensor object matching the provided sensor ID, or None if no matching sensor is found.

        Raises:
            None
        """
        with Session(self.engine) as session:

            result = session.exec(
                select(Sensors)
                .join(Records, Sensors.sensor_id == Records.sensor_id)
                .where(Sensors.sensor_id == sensor_id)
                .order_by(Records.updated_at.desc())
            ).first()

            # Call lazy query & oderder record starting from latest
            result.records = session.exec(
                select(Records)
                .where(Records.sensor_id == sensor_id)
                .order_by(Records.updated_at.desc())
                .limit(limit)
            ).all()
            return result

        
