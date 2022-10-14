from flask import Flask
from controllers.auth import auth
from controllers.proovedores import proovedores

from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(proovedores)

    app.config["JWT_SECRET_KEY"] = "uwu"  
    JWTManager(app)

    return app