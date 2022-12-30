import paho.mqtt.client as mqtt_client
import time


# BROKER = 'thingsboard.mosit'
BROKER = 'demo.thingsboard.io'
PORT = 1883
TOPIC = 'v1/devices/me/telemetry'


class IOT_device():
    def __init__(self, access_token):
        self.broker = BROKER
        self.port = PORT
        self.topic = TOPIC
        self.access_token = access_token

        self.connect()

    def connect(self):
        self.client = mqtt_client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.access_token)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def publish(self, message):
        message = str(message)
        result = self.client.publish(self.topic, message)
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)




def run():
    Humd = IOT_device('6vbwH7Tetl7EAG1SBpBW')
    time.sleep(1)

    # Noise = IOT_device('qFw8mLOF5mnh4qHvitLv')
    # time.sleep(1)
    #
    # Volt = IOT_device('uaqyokc5KWCkqZ0PlvKd')
    # time.sleep(1)


    Humd.publish({'humidity':200})
    time.sleep(1)
    # Noise.publish({'noise': 300})
    # time.sleep(1)
    # Volt.publish({'voltage': 400})
    # time.sleep(1)

   

if __name__ == '__main__':
    run()
