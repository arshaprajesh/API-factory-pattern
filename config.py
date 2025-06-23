class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:CK123indb#1@localhost/mechanic_service'
    DEBUG=True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEPOUT=300
    
class TestingConfig:
    pass    
class ProductionConfig:
    pass