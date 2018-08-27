class Config(object):
  """
  Common configureations
  """
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
  """
  Development configurations
  """
  DEBUG = True
 
  SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
  """
  Production configurations
  """

  DEBUG = False


app_config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig
}