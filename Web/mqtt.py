import paho.mqtt.client as mqtt
import os

# Define MQTT settings
mqtt_host = '127.0.0.1'
mqtt_port = 1883
mqtt_topic = 'my/topic'

# Define callback function for when a message is received
def on_message(client, userdata, msg):
    if msg.topic == mqtt_topic:
        # Run the video.py file
        print("hello")

# Create an MQTT client and connect to the broker
client = mqtt.Client()
client.connect(mqtt_host, 1883)

# Subscribe to the MQTT topic
client.subscribe(mqtt_topic)

# Set the callback function for when a message is received
client.on_message = on_message

# Start the MQTT client loop to listen for messages
client.loop_forever()
