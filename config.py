from os import environ
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"


class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")


# class DevelopmentConfig(Config):
#     """Development configuration."""

#     DB_HOST = environ.get("DB_HOST", "mariadb")
#     DB_USER = environ.get("DB_USER", "root")
#     DB_PASS = environ.get("DB_PASS", "")
#     DB_NAME = environ.get("DB_NAME", "api")
#     SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")

class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "")
    DB_USER = environ.get("DB_USER", "")
    DB_PASS = environ.get("DB_PASS", "")
    DB_NAME = environ.get("DB_NAME", "api")
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'database.db')


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")


config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)