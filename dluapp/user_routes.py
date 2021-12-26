from dluapp import app, db
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
from dluapp.forms import loginForm, createUserForm
from dluapp.models import Account, Character, CharacterData
from datetime import datetime
import logging
import pytz
import json

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', name=current_user.name)

@app.route('/leaderboards', methods=['GET'])
@login_required
def leaderboards():
    game_id_file = open('dluapp/activity_names.json')
    games = json.load(game_id_file)
    return render_template('leaderboards.html', name=current_user.name)