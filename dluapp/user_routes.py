from dispatchapp import app, db, presenceEngine
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from dispatchapp.config import Config
from dispatchapp.forms import loginForm, createUserForm, sendMessageForm
from dispatchapp.models import Call, User, Radio, RadioLocation, RadioCheckin
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime
from dispatchapp.const import ArsConst
import dispatchapp.turbo_common as turbo_common
import logging
import pytz

login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'fsudhfliuAEH32078SdhOUIHesogh045'
twilioClient = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_ACCOUNT_TOKEN)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
cst = pytz.timezone("US/Central")

presenceChecker = presenceEngine.PresenceEngine(interval=15, timeout=300)
presenceChecker.start()

@login.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', name=current_user.name)
