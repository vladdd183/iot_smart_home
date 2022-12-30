from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from routes.device_bp import device_bp
from routes.cmd_bp import cmd_bp
from models.Device import db

# from models.User import db
# from routes.user_bp import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userDB:passwordDB@db:5432/iotDB'
db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app, db)
#
# app.app_context().push()
# db.drop_all()
# db.create_all()
# db.session.commit()
app.register_blueprint(cmd_bp, url_prefix='/cmd')
app.register_blueprint(device_bp, url_prefix='/devices')

@app.route('/')
def index():
    return '<h1>hello</h1>'
    # return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
