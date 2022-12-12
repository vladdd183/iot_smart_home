from flask import Blueprint
from controllers.DeviceController import index, store


device_bp = Blueprint('device_bp', __name__)

device_bp.route('/', methods=['GET'])(index)
device_bp.route('/', methods=['POST'])(store)


