import paho.mqtt.client as mqtt
import time
from threading import Thread
import settings


# HOST = settings.MQTT_HOST
# PORT = settings.MQTT_PORT


HOST = 'oligroserver.ddns.net'
PORT = 1883


class Device(Thread):
    def __init__(self, name, topic):
        Thread.__init__(self, name=name)
        self.running = False
        self.client = mqtt.Client(client_id=name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(HOST, PORT)
        self.topic = topic

        self.data = {}

        self.running = True

        

    def run_function(self, fun, *args):
        Thread(target=fun, args=(*args,)).start()

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)

    def on_connect(self, client, userdata, flags, rc):
        self.subscribe(self.topic)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload)
 

class Light(Device):
    def __init__(self, name, topic):
        Device.__init__(self, name, topic)
        self.data = {'state': 'off',
                     'color': {'r': 0, 'g': 0, 'b': 0}}
        self.client.loop_start()

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        print('=================')
        match msg.split():
            case "on":
                self.data['state'] = 'on'
            case "off":
                self.data['state'] = 'off'
            case "set", "color", r, g, b:
                self.data['color']['r'] = int(r)
                self.data['color']['g'] = int(g)
                self.data['color']['b'] = int(b)
        self.publish(self.topic, self.data)


class Heater(Device):
    def __init__(self, name, topic):
        Device.__init__(self, name=name, topic=topic)
        self.data = {'temp': 0}
    
    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        match msg.split():
            case "quit":
                self.stop()
            case "set", x:
                self.data['temp'] = int(x)
            case "temp+", x:
                self.run_function(self.fct1, int(x))
            case "temp-", x:
                self.run_function(self.fct2, int(x))

    def fct1(self, x):
        while self.data['temp'] < x:
            self.data['temp'] += 1
            time.sleep(0.3)
            self.publish(self.topic+'/data', self.data)

    def fct2(self, x):
        while self.data['temp'] > x:
            self.data['temp'] -= 1
            time.sleep(0.3)
            self.publish(self.topic+'/data', self.data)



class TV(Device):
    def __init__(self, name, topic):
        Device.__init__(self, name, topic)
        self.data = {'state': 'off',
                     'channel': 0,
                     'volume': 0}

    def on_message(self, client, userdata, message):
        msg = message.payload.decode()
        msg = str(msg)
        print(msg)
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
        self.publish(self.topic, self.data)
