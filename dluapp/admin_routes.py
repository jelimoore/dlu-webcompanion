from dluapp import app, db
from flask import Flask, request, redirect, render_template, make_response, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
from dluapp.forms import loginForm, createUserForm
from dluapp.models import Account
from datetime import datetime
import logging
import pytz


@app.route('/admin', methods=['GET'])
@login_required
def admin_index():
    if (current_user.gm_level == 0):
        return redirect('/')
    return render_template('admin/index.html', name=current_user.name)
