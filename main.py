from uuid import UUID

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

from config import Config
from controllers.account_controller import account
from controllers.user_controller import user
from models import db, User
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(UUID(user_id))


app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(account, url_prefix='/account')

if __name__ == "__main__":
    app.run(debug=False)