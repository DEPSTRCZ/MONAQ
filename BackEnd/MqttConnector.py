import paho.mqtt.client as mqtt
import json
import re
from DataBaseConnector import DataBaseConnector


class MqttConnector:
    def __init__(self):
        USERNAME = "REDACTED"
        PASSWORD = "REDACTED"
        SERVER = "REDACTED"
        PORT = 8883

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.username_pw_set(USERNAME, PASSWORD)
        self.mqttc.tls_set()
        self.mqttc.connect(SERVER, PORT, 60)


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected with result code", reason_code)
            client.subscribe("/#", qos=1)  # Subscribe to all topics with QoS 1 (at least once delivery)
        else:
            print(f"Connection failed, return code: {reason_code}")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        #print(Buffer)

            # Parse topic & split it at /
            topic_split = (msg.topic).split("/")


            #print(msg.topic)
            #print(" ")

            if re.search(r"/co2/|-co-",msg.topic):
                # Parse payload to json
                payload = json.loads(msg.payload.decode())
                # Get the raw sensor data
                sensor_data = payload["uplink_message"]["decoded_payload"]["msg"].split(";")
                if not sensor_data:
                    print("ERROR")
                sid,co2,temperature,humidity = sensor_data
                # Get the location data of the sensor
                location = payload["uplink_message"]["rx_metadata"][0]["location"]
                lat,long = location["latitude"],location["longitude"]
                # Put together an data object
                data = {"id":sid,"updated_at":payload["received_at"],"co2":co2,"temperature":temperature,"humidity":humidity,"loc_lat":lat,"loc_long":long}
                #print(data)
                # Append to db
                print("saved",msg.topic)
                DataBaseConnector().SaveRecord(data)
    def run(self):
        self.mqttc.loop_forever()

