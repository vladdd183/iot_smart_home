import paho.mqtt.client as mqtt
import time
import os
from threading import Thread
import settings
from flask_sqlalchemy import SQLAlchemy
# from models.Device import Logger

db = SQLAlchemy()

HOST = settings.MQTT_HOST
PORT = settings.MQTT_PORT

class Device(Thread):
    def __init__(self, name, topic):
        Thread.__init__(self, name=name)
        self.running = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(HOST, PORT)
        self.client.loop_start()
        self.topic = topic

        if not self.data:
            self.data = {}

        self.running = True

        self.run()

    def log(self, log_data= "No log data"):
        log_string = Logger(self.topic, self.name, self.data, log_data)
        db.session.add(log_string)
        db.session.commit()
         
    def run_function(self, fun, *args):
        Thread(target=fun, args=(*args,)).start()

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        log_data = "Received message '" + msg + "' on topic '" + self.topic + "' with QoS " + str(message.qos)
        self.log(log_data)

    def on_connect(self, client, userdata, flags, rc):
        log_data = "connected"
        self.log(log_data)
        self.subscribe(self.topic+"/cmd")

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload)


    def run(self):
        old_data = self.data.copy()
        while self.running:
            if old_data != self.data:
                self.publish(self.topic, str(self.data))
                old_data = self.data.copy()
            time.sleep(1)

    def stop(self):
        if self.running:
            self.running = False

            self.join()

            print("Ending and cleaning up")
            self.client.disconnect()



class Light(Device):
    def __init__(self, name, topic):
        self.data = {'state': 'off',
                     'color': {'r': 0, 'g': 0, 'b': 0}}
        Device.__init__(self, name, topic)

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        log_data = "Received message '" + msg + "' on topic '" + self.topic + "' with QoS " + str(message.qos)
        self.log(log_data)
        match msg.split():
            case "quit":
                self.stop()
            case "on":
                self.data['state'] = 'on'
            case "off":
                self.data['state'] = 'off'
            case "set", "color", r, g, b:
                self.data['color']['r'] = int(r)
                self.data['color']['g'] = int(g)
                self.data['color']['b'] = int(b)


class Heater(Device):
    def __init__(self, name, topic):
        self.data = {'temp': 0}
        Device.__init__(self, name=name, topic=topic)
    
    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        log_data = "Received message '" + msg + "' on topic '" + self.topic + "' with QoS " + str(message.qos)
        self.log(log_data)
        match msg.split():
            case "quit":
                self.stop()
            case "set", x:
                self.data['temp'] = int(x)
            case "temp+", x:
                self.run_function(self.fct1, int(x))
            case "temp-", x:
                self.run_function(self.fct1, int(x))

    def fct1(self, x):
        while self.data['temp'] < x:
            self.data['temp'] += 1
            time.sleep(0.3)

    def fct2(self, x):
        while self.data['temp'] > x:
            self.data['temp'] -= 1
            time.sleep(0.3)



class TV(Device):
    def __init__(self, name, topic):
        self.data = {'state': 'off',
                     'channel': 0,
                     'volume': 0}
        Device.__init__(self, name, topic)

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        log_data = "Received message '" + msg + "' on topic '" + self.topic + "' with QoS " + str(message.qos)
        self.log(log_data)
        match msg.split():
            case "quit":
                self.stop()
            case "on":
                self.data['state'] = 'on'
            case "off":
                self.data['state'] = 'off'
            case "set", "channel", channel:
                self.data['channel'] = int(channel)
            case "set", "volume", volume:
                self.data['volume'] = int(volume)
            case "channel+":
                self.data['channel'] += 1
            case "channel-":
                self.data['channel'] -= 1
            case "volume+":
                self.data['volume'] += 1
            case "volume-":
                self.data['volume'] -= 1
