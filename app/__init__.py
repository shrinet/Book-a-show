import os
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, current_app
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app.config.settings import BaseConfig, DevConfig, ProductionConfig, TestingConfig


metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
admin = Admin(name='Dashboard')
migrate = Migrate()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
bootstrap = Bootstrap()
moment = Moment()


def create_app():
    
    app = Flask(__name__, static_folder='static', template_folder='templates')
    if os.getenv('ENV', "development") == "production":
      app.config.from_object(ProductionConfig)      
    elif os.getenv('ENV', "development") == "testing":
      app.logger.info("Staring Testing.")
      print("Staring Testing")
      app.config.from_object(TestingConfig)      
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(DevConfig)

    # initialize SQLAlchemy
    db.init_app(app)
    
    
    migrate.init_app(app, db, render_as_batch=True)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.app_context().push()

   

    return app

from app import models

