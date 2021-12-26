from dluapp import app, db
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
from dluapp.forms import loginForm, createUserForm, activateForm
from dluapp.models import Account
from datetime import datetime
import logging
import pytz

login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'fsudhfliuAEH32078SdhOUIHesogh045'


@login.user_loader
def load_user(id):
    return Account.query.get(id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(redirect('/'))
    form = loginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', title='Sign In', form=form, signInFail=True)
        login_user(user, remember=form.rememberMe.data)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/activate', methods=['GET', 'POST'])
def activateAccount():
    if current_user.is_authenticated:
        return 'Cannot create new account while you are already logged in'
    form = activateForm()
    if form.validate_on_submit():
        error = None
        user = Account.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('activate.html', title='Sign In', form=form, signInFail=True)
        login_user(user, remember=form.rememberMe.data)
        return redirect('/')
    return render_template('activate.html', title='Activate Account', form=form)

@app.route('/createAccount', methods=['GET', 'POST'])
@login_required
def createAccount():
    if (current_user.gm_level == 9):
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
