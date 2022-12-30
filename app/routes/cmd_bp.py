
from flask import Blueprint
from controllers.DeviceController import cmd


cmd_bp = Blueprint('cmd_bp', __name__)

cmd_bp.route('/', methods=['POST'])(cmd)
