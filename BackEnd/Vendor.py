from MqttConnector import MqttConnector
from DataBaseConnector import DataBaseConnector
from sqlmodel import Field, SQLModel, create_engine

connector = DataBaseConnector()
#SQLModel.metadata.create_all(connector.engine)

MqttConnector().run()
#db = DataBaseConnector()
#db.GetSensors()