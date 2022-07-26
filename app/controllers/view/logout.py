from app import app, config,db
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
from werkzeug.security import generate_password_hash,check_password_hash


# Models
from app.models.modelsflask import User, user, users, UsersPassword, userPassword, userPasswords,UsersRole,userRole,userRoles

@app.route('/logout', methods=['get'])
def logout():
    del session['email']
    del session['session']
    # session.clear()
    return redirect(url_for('index'))