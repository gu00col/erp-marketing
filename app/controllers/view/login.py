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

@app.route('/login', methods=['POST'])
def login():
    # if form is submited
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Validar se o login existe no banco
        
        consulta_login = db.session.query(User).filter_by(email=email).first()
        # Se não existe o e-mail retorna para a index com mensagem de erro
        if not consulta_login:
            flash('Email não encontrado.','error')
            return redirect(url_for('index'))

        # Validamos se o usuario está ativo

        if not consulta_login.active:
            # Retorne para a página e envie mensagem de erro
            flash('Sua conta está inativa, entre em contato com o o suporte para verificar o motivo.','error')
            return redirect(url_for('index'))

        
        # Devemos validar a senha

        consulta_senha = db.session.query(UsersPassword).filter(UsersPassword.users_email==email and UsersPassword.active==1).first()

        if not consulta_senha:
            # Se não foi encontrado senha ativa ou senha não tem senha cadastrada retorna para tela de login com mensagem
            flash('Senha incorreta. Se você se esqueceu sua senha clique em esqueci minha senha.','error')
            return redirect(url_for('index'))

        # Se existe senha ativa devemos comapra a senha passada.

        senha = check_password_hash(consulta_senha.password, password)

        if not senha:
            flash('Senha incorreta. Se você se esqueceu sua senha clique em esqueci minha senha.','error')
            return redirect(url_for('index'))

        # Usuario e senha corretos

        consulta_acessos = db.session.query(UsersRole).filter(UsersRole.users_id==consulta_login.id).all()
        consulta_acessos_json = userRoles.dump(consulta_acessos)

        sessao = {
            "user_name" : consulta_login.user_name,
            "name" : consulta_login.name,
            "email" : consulta_login.email,
            "user_roles " : consulta_acessos_json

        }
       
        session["email"] = consulta_login.email
        session['session'] = sessao
    
        return redirect(url_for('home'))