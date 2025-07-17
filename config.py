import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:CK123indb#1@localhost/mechanic_service'
    DEBUG=True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEPOUT=300
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'  
    CACHE_DEFAULT_TIMEPOUT=300  
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','postgresql+psycopg://root:CK123indb#1@localhost/mechanic_service')
    CACHE_TYPE = "SimpleCache"