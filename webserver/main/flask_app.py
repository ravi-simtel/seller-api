import os

from main.models import BaseModel
file = os.path.dirname(os.path.dirname('.env_dev'))
from dotenv import load_dotenv

load_dotenv(file)

def create_app(config_name):
    from flask import Flask
    from main.config import config_by_name

    app = Flask(__name__, template_folder='templates', static_url_path='')
    app.config.from_object(config_by_name[config_name])
    app.app_context().push()
    model = BaseModel()
    return app


app = create_app(os.getenv("ENV") or "dev")
