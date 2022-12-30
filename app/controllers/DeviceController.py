from flask import render_template, request
from models.Device import Device
import controllers.iot as iot
from threading import Thread
import paho.mqtt.publish as publish
import settings
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()




def dev_init(dev, name, topic):
    match dev:
        case 'heater':
            device = iot.Heater
        case 'tv':
            device = iot.TV
        case 'lamp':
            device = iot.Light
        case _:
            device = iot.Device

    dev = Device(name, topic, dev)
    device = device(name, topic)
    db.session.add(dev)
    db.session.commit()
    


def index():
    devices = Device.query.all()
    return str(devices)
    # return render_template('devices/index.html', devices=devices)

def store():
    name = request.form['name'] or None
    topic = request.form['topic'] or None
    dev_type = request.form['dev_type'] or None
    if all([name, topic, dev_type]):
        dev_init(dev_type, name, topic)
        return 'Device created'
    return 'error'

def cmd():
    cmd = request.form['cmd']
    topic = request.form['topic']
    publish.single(topic=topic+'/cmd', payload=cmd, hostname=settings.MQTT_HOST, port=settings.MQTT_PORT)
    return 'ok'
