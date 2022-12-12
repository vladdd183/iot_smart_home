from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Logger(db.Model):
    __tablename__ = 'logs'
    topic = db.Column(db.String(255),primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(255), nullable=True)
    log_data = db.Column(db.String(255), nullable=True)
    timestemp = db.Column(db.String(255), nullable=False)

    def __init__(self, name, topic, data: None, log_data: None):
        self.topic = topic 
        self.data = data
        self.name = name
        self.log_data = log_data
