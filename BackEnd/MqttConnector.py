import paho.mqtt.client as mqtt
import json
import re
from DataBaseConnector import DataBaseConnector


class MqttConnector:
    def __init__(self):
        """
        Initializes a new instance of the class.

        This method sets up the MQTT client with the provided username, password, server, and port. It also sets the callback functions for connection and message handling. Finally, it connects to the MQTT server.

        Parameters:
            None

        Returns:
            None
        """
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
        """
        The callback function for when the client receives a CONNACK response from the server.
        
        Parameters:
            client (mqtt.Client): The MQTT client instance for this callback.
            reason_code (int): The connection result.

        
        Returns:
            None
        
        This function is called when the client has successfully connected to the broker.
        If the reason code is 0, it means the connection was successful.
        In this case, it subscribes to all topics with QoS 1 (at least once delivery).
        If the reason code is not 0, it means the connection failed.
        In this case, it prints the connection failure message.
        """
        if reason_code == 0:
            print("Connected with result code", reason_code)
            client.subscribe("/#", qos=1)  # Subscribe to all topics with QoS 1 (at least once delivery)
        else:
            print(f"Connection failed, return code: {reason_code}")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        """
        Callback function for when a PUBLISH message is received from the server.

        Args:
            msg (mqtt.MQTTMessage): The received message.

        Returns:
            None

        This function parses the topic of the received message and splits it at the "/" character.
        If the topic matches the pattern "/co2/" or "-co-", it parses the payload of the message as JSON.
        It extracts the sensor data from the decoded payload and the location data from the received metadata.
        It then constructs a data object with the extracted data and saves it to the database using the DataBaseConnector class.
        The function prints a message indicating the topic of the saved message.
        """
        print(msg.topic)
        if re.search(r"/co2/|-co-",msg.topic):
            try:
            # Parse payload to json
                payload = json.loads(msg.payload.decode())
                # Get the raw sensor data
                if "msg" in payload["uplink_message"]["decoded_payload"]:
                    sensor_data = payload["uplink_message"]["decoded_payload"]["msg"].split(";")
                else:
                    sensor_data = payload["uplink_message"]["decoded_payload"]["payload"].split(";")

                sid,co2,temperature,humidity = sensor_data
                # Get the location data of the sensor
                if "location" in payload["uplink_message"]["rx_metadata"][0]:
                    location = payload["uplink_message"]["rx_metadata"][0]["location"]
                    lat,long = location["latitude"],location["longitude"]
                else:
                    lat,long = 0,0
                # Put together an data object
                data = {"id":sid,"updated_at":payload["received_at"],"co2":co2,"temperature":temperature,"humidity":humidity,"loc_lat":lat,"loc_long":long}
                #print(data)
                # Append to db
                print("saved",msg.topic)
                DataBaseConnector().SaveRecord(data)
            except Exception as e:
                print("failed to save",msg.topic)
                print(e)
                print(msg.payload)
    def run(self):
        self.mqttc.loop_forever()

