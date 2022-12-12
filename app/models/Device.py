from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Device(db.Model):
    __tablename__ = 'devices'
    topic = db.Column(db.String(255),primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(255), nullable=True)
    dev_type = db.Column(db.String(255), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('devices', lazy=True))
    # user = db.relationship('User', backref=db.backref('devices', lazy=True))

    def __init__(self, name, topic, dev_type):
        self.name = name
        self.topic = topic
        self.dev_type = dev_type

class Logger(db.Model):
    __tablename__ = 'logs'
    topic = db.Column(db.String(255), db.ForeignKey('Device.topic'))
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(255), nullable=True)
    log_data = db.Column(db.String(255), nullable=True)
    timestemp = db.Column(db.String(255),primary_key=True)

    def __init__(self, name, topic, data: None, log_data: None):
        self.topic = topic 
        self.data = data
        self.name = name
        self.log_data = log_data
