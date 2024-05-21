from flask_jwt_extended import JWTManager, create_access_token

class TokenManager:
    def __init__(self, app, secret_key):
        app.config['JWT_SECRET_KEY'] = secret_key
        self.jwt = JWTManager(app)

    def generate_token(self, identity):
        return create_access_token(identity=identity)