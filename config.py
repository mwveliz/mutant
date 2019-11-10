from dotenv import load_dotenv
import os
class Config(object):
  load_dotenv()
  PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
  SERVER=os.getenv("SERVER")
  DATABASE = os.path.join(PROJECT_ROOT, 'db', os.getenv("DATABASE"))
  # Statement for enabling the development environment
  DEBUG = True
  # Define the application directory
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))

  JSON_AS_ASCII = False


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass
