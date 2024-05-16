from flask import Flask
from flask_login import LoginManager
from models.user_model import db, User
from controllers.user_controller import user
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'finances.db')
app.config['SECRET_KEY'] = 'ghsdfgdshgfdhjsdfgghdf4g5645fdg54df65gf6'

db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
