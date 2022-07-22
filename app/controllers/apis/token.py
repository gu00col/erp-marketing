from app import api, config, config, db, ma,secret_key
# from app.resources.teste import Teste
from flask_restful import Resource, reqparse
from pymysql.err import MySQLError
import requests
import simplejson as json
import time
import datetime
from dateutil.parser import parse
import bcrypt
import base64
import time
import sys
from datetime import datetime, timedelta
from ast import literal_eval
import re
import jwt


class Teste(Resource):

    args = reqparse.RequestParser()
    args.add_argument('user_name',required=True,help='O parametro user_name é obrigatório no json!')
    args.add_argument('email',required=True,help='O parametro email é obrigatório no json!')

    def post(self):
        args = Teste.args.parse_args()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        payload = {
            "user_name" : args['user_name'],
            "email" : args['email'],
            "created_at" : now,
            'exp' : datetime.datetime.now() + datetime.timedelta(hours=12)
        }
        token = jwt.encode(payload,secret_key).decode("utf-8")

        return {"token" : token},200

api.add_resource(Teste, '/api/v1/token')