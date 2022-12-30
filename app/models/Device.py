from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Device(db.Model):
    __tablename__ = 'devices'
    topic = db.Column(db.String(255),primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dev_type = db.Column(db.String(255), nullable=False)

    def __init__(self, name, topic, dev_type):
        self.name = name
        self.topic = topic
        self.dev_type = dev_type

