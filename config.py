class Config(object):
  """
  Common configureations
  """
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  DEBUG = True

class DevelopmentConfig(Config):
  """
  Development configurations
  """
 
  SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
  """
  Production configurations
  """

  DEBUG = False

class TestingConfig(Config):
  """
  Testing configurations
  """

  TESTING = True


app_config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig
}