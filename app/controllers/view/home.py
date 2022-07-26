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


# Models
from app.models.modelsflask import Menu, MenuItem, menuItem, menuItems, menu, menus

@app.route('/home', methods=['GET'])
def home():
    # Validar Sessão
    # check if the users exist or not
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        flash('Você não está logado!','error')
        return redirect("/")


    # menus

    consulta_menu_principal = db.session.query(MenuItem).join(Menu, Menu.id == MenuItem.menus_id).filter(Menu.name== 'principal').all()

    return render_template('home.html', titulo='Home - ASDIGITAL', session=session.get("session"),menu_principal=consulta_menu_principal)