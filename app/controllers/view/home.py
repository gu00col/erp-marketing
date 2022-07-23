from app import app, config
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
import requests
import simplejson as json
import time
import datetime
from dateutil.parser import parse
import bcrypt
import base64
import time
import sys
import datetime
from datetime import datetime, timedelta


@app.route('/home', methods=['GET'])
def home():
    # Validar Sessão
    # check if the users exist or not
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        flash('Você não está logado!','error')
        return redirect("/")

    return render_template('home.html', titulo='Home - ASDIGITAL', session=session.get("session"))