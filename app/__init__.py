from os import environ
from flask import Flask
from app.controllers.auth import auth
from app.controllers.proovedores import proovedores 
from app.controllers.solicitudes import solicitudes
from app.controllers.materiales import materiales
from flask_swagger_ui import get_swaggerui_blueprint

from flask_jwt_extended import JWTManager
from app import db
from config import config

def create_app(environment="development"):
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(proovedores)
    app.register_blueprint(solicitudes)
    app.register_blueprint(materiales)

    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Documento Swagger"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)


    # JWT
    app.config["JWT_SECRET_KEY"] = "uwu"  
    JWTManager(app)

    # Database
    db.init_db(app)
    return app