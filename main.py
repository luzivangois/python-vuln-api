from flask import Flask
from flask_login import LoginManager

from controllers.account_controller import account
from models import db, User
from controllers.user_controller import user
import os

from utils.token_service import TokenManager

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'invest.db')
app.config['SECRET_KEY'] = 'ghsdfgdshgfdhjsdfgghdf4g5645fdg54df65gf6'
token_manager = TokenManager(app, '1213265115156132165156156155653156')

db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(account, url_prefix='/account')

if __name__ == "__main__":
    app.run(debug=True)