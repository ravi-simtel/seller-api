import os
from datetime import timedelta
from dotenv import load_dotenv 

BASE_DIR = os.path.join(os.path.dirname( os.path.dirname( __file__ )), '.env' )
print(BASE_DIR)
load_dotenv(BASE_DIR)

class Config:
    OTP_TIMEOUT_IN_MINUTES = 60
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_ACCESS_SECRET = os.getenv('AWS_ACCESS_SECRET')

    DEBUG = False
    COOKIE_EXPIRY = 60000
    PORT = 3021
    FLASKS3_BUCKET_NAME = os.getenv('STATIC_BUCKET_NAME')
    FLASKS3_FILEPATH_HEADERS = {r'.css$': {'Content-Type': 'text/css; charset=utf-8'},
                                r'.js$': {'Content-Type': 'text/javascript'}}
    FLASKS3_ACTIVE = os.getenv("flask_s3_active", "True") == "True"
    FLASKS3_GZIP = True
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    JWT_TOKEN_LOCATION = ['headers']
    # below is valid for tokens coming in as part of query_params
    JWT_QUERY_STRING_NAME = "token"
    # Set the secret key to sign the JWTs with
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DOMAIN = "ONDC:RET14"
    CITY_CODE = "std:080"
    COUNTRY_CODE = "IND"
    BAP_TTL = "20"
    BECKN_SECURITY_ENABLED = False
    SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE"))
    BPP_PRIVATE_KEY = os.getenv("BPP_PRIVATE_KEY")
    BPP_PUBLIC_KEY = os.getenv("BPP_PUBLIC_KEY")
    BPP_ID = os.getenv("BPP_ID")
    BPP_URI = os.getenv("BPP_URI")
    BPP_UNIQUE_KEY_ID = os.getenv("BPP_UNIQUE_KEY_ID")
    BPP_CLIENT_ENDPOINT = os.getenv("BPP_CLIENT_ENDPOINT")
    IGM_CLIENT_ENDPOINT = os.getenv(
        "IGM_CLIENT_ENDPOINT")
    BG_DEFAULT_URL = os.getenv("BG_DEFAULT_URL")
    BG_DEFAULT_URL_FLAG = os.getenv("BG_DEFAULT_URL_FLAG")
    LOGISTICS_ON_SEARCH_WAIT = int(os.getenv("LOGISTICS_ON_SEARCH_WAIT"))
    print(LOGISTICS_ON_SEARCH_WAIT)
    TTL_IN_SECONDS = int(os.getenv("TTL_IN_SECONDS", "3600"))
    VERIFICATION_ENABLE = os.getenv("VERIFICATION_ENABLE")
    REGISTRY_BASE_URL = os.getenv("REGISTRY_BASE_URL")
    SECRET_KEY=os.getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    BASE_DIR = os.path.join(os.path.dirname( os.path.dirname( __file__ )), '.env' )
    print(BASE_DIR)
    load_dotenv(BASE_DIR)
    DEBUG = True
    ENV = True
    RABBITMQ_HOST = "localhost"
    MONGO_DATABASE_SRV="mongodb://localhost:27017/"
    #MONGO_DATABASE_SRV = os.getenv("MONGO_DATABASE_SRV")

class ProductionConfig(Config):
    BASE_DIR = os.path.join(os.path.dirname( os.path.dirname( __file__ )), '.env' )
    print(BASE_DIR)
    load_dotenv(BASE_DIR)
    
    DEBUG = False
    RABBITMQ_HOST = "rabbitmq"
    MONGO_DATABASE_SRV = os.getenv("MONGO_DATABASE_SRV")
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")


class PreProductionConfig(Config):
    BASE_DIR = os.path.join(os.path.dirname( os.path.dirname( __file__ )), '.env' )
    print(BASE_DIR)
    load_dotenv(BASE_DIR)
    
    DEBUG = False
    RABBITMQ_HOST = "rabbitmq"
    MONGO_DATABASE_SRV= os.getenv("MONGO_DATABASE_SRV")
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    pre_prod=PreProductionConfig,
)

key = Config.SECRET_KEY


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv("ENV")
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value


def get_email_config_value_for_name(config_name):
    email_config_value = get_config_by_name("SES") or {}
    config = email_config_value.get(config_name)
    return config
