from dluapp import app, db
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
from dluapp.forms import loginForm, createUserForm, activateForm
from dluapp.models import Account, PlayKey
from datetime import datetime
import logging
import pytz

login = LoginManager(app)
login.login_view = 'login'


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
    message = None
    error = None
    if current_user.is_authenticated:
        return 'Cannot create new account while you are already logged in'
    form = activateForm()
    if form.validate_on_submit():
        # check that the play key exists, is active, and has at least one use
        playkey = PlayKey.query.filter_by(key_string=form.play_key.data).first()
        if playkey is None or playkey.active==0 or playkey.key_uses==0:
            error = "Invalid Play Key."
        else:
            # decrement the key uses
            playkey.key_uses -= 1
            # check that the username doesn't already exist
            user = Account.query.filter_by(name=form.name.data).first()
            if user is None:
                # again for the email
                user = Account.query.filter_by(email=form.email.data).first()
                if user is None:
                    # check that both passwords match
                    if (form.password.data == form.password2.data):
                        user = Account(email=form.email.data, name=form.name.data, gm_level=0, locked=0, banned=0, play_key_id=playkey.id, mute_expire=0)
                        user.set_password(form.password.data)
                        db.session.add(user)
                        db.session.commit()
                        message = "Successfully created account."
                    else:
                        error = "Passwords do not match."
                else:
                    error = "Email already exists."
            else:
                error = "That username already exists."
        
    return render_template('activate.html', form=form, message=message, error=error)

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
