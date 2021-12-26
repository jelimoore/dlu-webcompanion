from dispatchapp import app, db, presenceEngine
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from dispatchapp.config import Config
from dispatchapp.forms import loginForm, createUserForm, sendMessageForm
from dispatchapp.models import Call, User, Radio, RadioLocation, RadioCheckin
from datetime import datetime
from dispatchapp.const import ArsConst
import dispatchapp.turbo_common as turbo_common
import logging
import pytz

login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'fsudhfliuAEH32078SdhOUIHesogh045'


@login.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(redirect('/'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', title='Sign In', form=form, signInFail=True)
        login_user(user, remember=form.rememberMe.data)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/createAccount', methods=['GET', 'POST'])
@login_required
def createAccount():
    #if (current_user.serviceLevel == 99):
    if True:
        form = createUserForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                return(redirect('/createAccount'))
            user = User(email=form.email.data, name=form.name.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        return render_template('createAccount.html', title='Create Account', form=form)
    else:
        return '401 Unauthorized', 401
