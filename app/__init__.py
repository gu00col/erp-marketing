from flask import Flask
from flask_session import Session
from flask_cors import CORS
from flask_restful import Api
import simplejson as json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os
from os.path import join, dirname
import time
import dateutil
from flask_caching import Cache
from datetime import timedelta
from flask_mail import Mail, Message

# Carregamentos de variaveis env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# loggs
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Cache 
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


# Key
import string
import random
key_srt = string.ascii_letters + string.digits + string.ascii_uppercase
key_random = ''.join(random.choice(key_srt) for _ in range(12))
key_random2 = ''.join(random.choice(key_srt) for _ in range(8))

# Configs
app = Flask(__name__)

# Configuração CACHE
app.config.from_mapping(config)
cache = Cache(app)

# Configuração de arquivos flask
app.config['BUNDLE_ERRORS'] = True
app.config['UPLOAD_FOLDER'] = "./static/uploads"

# Configuração para retorno dos JSON
app.config['JSON_SORT_KEYS'] = False

# Configuração de sessão flask
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "lax"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)
session = Session(app)

# Configuração da API REST FULL
api = Api(app)
CORS(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
secret_key = app.config['SECRET_KEY'] = key_random
api_key = '''@u20#tesl@2019_n4p@'''

# Banco dados
app.config['SLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app,  engine_options={ 'connect_args': { 'connect_timeout': 1400},"pool_recycle": 120})
engine_container = db.get_engine(app)

# Serialização
ma = Marshmallow(app)

# funçõs decorator de template
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d.%m.%y %H:%m'
    return date.strftime(format)

@app.template_filter('data')
def data(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d.%m.%y'
    return date.strftime(format) 

# Email
# mail = Mail()

# app.config['MAIL_SERVER']='servidor'
# app.config['MAIL_PORT'] = porta
# app.config['MAIL_USERNAME'] = 'email'
# app.config['MAIL_PASSWORD'] = 'senha'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True


# mail.init_app(app)

#           Importando as rotas api
# from app.controllers.apis import login, auth,first_login, logout, users
# Importando as rotas de WebView
from app.controllers.view import default
