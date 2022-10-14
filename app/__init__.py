from os import environ
from flask import Flask
from app.controllers.auth import auth
from app.controllers.proovedores import proovedores 
from flask_jwt_extended import JWTManager
from app import db
from config import config

def create_app(environment="development"):
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(proovedores)

    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # JWT
    app.config["JWT_SECRET_KEY"] = "uwu"  
    JWTManager(app)

    # Database
    db.init_db(app)
    return app