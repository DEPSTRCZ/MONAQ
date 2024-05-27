import paho.mqtt.client as mqtt
import json
# Buffer



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected with result code", reason_code)
        client.subscribe("/#", qos=1)  # Subscribe to all topics with QoS 1 (at least once delivery)
    else:
        print(f"Connection failed, return code: {reason_code}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(Buffer)

    #try:
        # Parse topic & split it at /
        topic_split = (msg.topic).split("/")

        if len(topic_split) > 4:
            if topic_split[1] == "ttndata":
                if topic_split[4] == "co2":
                    # Parse payload to json
                    payload = json.loads(msg.payload.decode())
                    # Get the raw sensor data
                    sensor_data = payload["uplink_message"]["decoded_payload"]["msg"].split(";")
                    sid,co2,tempature,humidity = sensor_data
                    # Get the location data of the sensor
                    location = payload["uplink_message"]["rx_metadata"][0]["location"]
                    lat,long = location["latitude"],location["longitude"]
                    # Put together an data object
                    data = {"id":sid,"updated_at":payload["received_at"],"co2":co2,"temperature":tempature,"humidity":humidity,"lat":lat,"long":long}
                    print(data)
                    # Append to buffer¨



mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("REDACTED","REDACTED")
mqttc.tls_set()
mqttc.connect("REDACTED", 8883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
# čislo s, co2 koncen, teplota, vlhkost 