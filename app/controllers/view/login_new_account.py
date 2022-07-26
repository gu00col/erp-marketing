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

@app.route('/new_account', methods=['GET','POST'])
def login_new_account():

    # if form is submited
    if request.method == "POST":
        email = request.form['email']
        # Validação se os dados de e-mail foi passado
        if email == None or email == '':

            flash('Email passado não é valido!','error')

            return redirect(url_for('password_recovery'))
        
        # Verificando no banco se existe o email

        consulta_email = db.session.query(User).filter(User.email == email).first()
        consulta_email = user.dump(consulta_email)
        if not consulta_email:
            flash('Email não encontrado.','error')
            print('Aqui')
            return redirect(url_for('password_recovery'))

        flash('Email de recuperação enviado.','success')
        return redirect(url_for('index'))

    return render_template('login_new_account.html', titulo='Nova conta - ASDIGITAL')