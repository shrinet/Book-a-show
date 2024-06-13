import os
class BaseConfig():
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
   DEBUG = True
   BASE_DIR = os.path.abspath(os.path.dirname('..'))
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
   SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
   UPLOADED_FILES = os.path.join(BASE_DIR,'app/static')
   SECURITY_FRESHNESS_GRACE_PERIOD = 6000
   

class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   BASE_DIR = os.path.abspath(os.path.dirname(__file__))
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app_prod.db')
   SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')