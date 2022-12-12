from flask import render_template, request
from models.Device import Device
import controllers.iot as iot
from threading import Thread
import paho.mqtt.publish as publish

from flask_sqlalchemy import SQLAlchemy
import settings
HOST = settings.MQTT_HOST

def dev_init(dev, name, topic):
    Thread(target=dev, args=(name, topic,)).start()
db = SQLAlchemy()

def index():
    devices = Device.query.all()
    return str(devices)
    # return render_template('devices/index.html', devices=devices)

def store():
    name = request.form['name'] or None
    topic = request.form['topic'] or None
    dev_type = request.form['dev_type'] or None
    if all([name, topic, dev_type]):
        match dev_type:
            case 'heater':
                device = iot.Heater
                dev_init(device,name,topic)
            case 'tv':
                device = iot.TV
                dev_init(iot.TV,name,topic)
            case 'light':
                device = iot.Light
                dev_init(iot.Light,name,topic)
            case _:
                device = iot.Device
                dev_init(iot.Device,name, topic)
        db.session.add(device)
        db.session.commit()
        return 'Device created'
    return 'error'

def cmd():
    print('1'*100)
    print(request.form)

    cmd = request.form['cmd']
    topic = request.form['topic']
    publish.single(topic, cmd, hostname=HOST)    
    return 'ok' 
