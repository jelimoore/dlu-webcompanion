from dluapp import app, db
from flask import Flask, request, redirect, render_template, make_response, jsonify, Response
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
from dluapp.forms import renameCharacterForm
from dluapp.models import Account, Character, CharacterData, Leaderboard
from datetime import datetime
import logging
import pytz
import json
import time

@app.route('/', methods=['GET'])
@login_required
def index():
    #snag all the characters from the db
    chars = Character.query.filter_by(account_id=current_user.id).all()
    return render_template('index.html', characters=chars)

@app.route('/characters/<id>', methods=['GET', 'POST'])
@login_required
def character_info(id):
    form = renameCharacterForm()
    if form.validate_on_submit():
        #grab the ID requested and verify the account logged in has permission to edit it
        character = Character.query.filter_by(id=id).filter_by(account_id=current_user.id).first()
        if character is not None:
            character.pending_name = form.requested_name.data
            db.session.commit()
    #snag all the characters from the db
    #important that we do this after the change so the new name shows up
    char = Character.query.filter_by(id=id).filter_by(account_id=current_user.id).first()
    return render_template('charinfo.html', character=char, form=form)

@app.route('/download_charxml', methods=['GET'])
@login_required
def download_charxml():
    requested_id = request.args.get('id')
    #TODO: make sure that this account is authorized to download that user's info
    charxml = CharacterData.query.filter_by(id=requested_id).first()
    return Response(charxml.xml_data, mimetype='text/plain')

@app.route('/leaderboards', methods=['GET'])
@login_required
def leaderboards():
    game_id_file = open('dluapp/activity_names.json')
    games = json.load(game_id_file)
    leaderboards = list()
    # iterate through all games in the json file
    for game in games['activities']:
        gameid = game['id']
        player_scores = list()
        # value header for the table
        value_header = ""
        # switch based on how we sort the games and what by
        if (game['sort'] == 'asc' and game['sort_by'] == 'time'):
            players = Leaderboard.query.filter_by(game_id=gameid).order_by(Leaderboard.time.asc()).limit(10).all()
            value_header = "Time (mm:ss)"

            #iterate through the players, and add just the necessary info to a new dict
            for player in players:
                player_score = dict()
                player_score['name'] = player.character.name
                player_score['value'] = time.strftime('%M:%S', time.gmtime(player.time))
                player_scores.append(player_score)
            
        elif (game['sort'] == 'desc' and game['sort_by'] == 'time'):
            players = Leaderboard.query.filter_by(game_id=gameid).order_by(Leaderboard.time.desc()).limit(10).all()
            value_header = "Time (mm:ss)"

            #iterate through the players, and add just the necessary info to a new dict
            for player in players:
                player_score = dict()
                player_score['name'] = player.character.name
                player_score['value'] = time.strftime('%M:%S', time.gmtime(player.time))
                player_scores.append(player_score)
            
        elif (game['sort'] == 'desc' and game['sort_by'] == 'score'):
            players = Leaderboard.query.filter_by(game_id=gameid).order_by(Leaderboard.score.desc()).limit(10).all()
            value_header = "Score"

            #iterate through the players, and add just the necessary info to a new dict
            for player in players:
                player_score = dict()
                player_score['name'] = player.character.name
                player_score['value'] = "{:,}".format(player.score)
                player_scores.append(player_score)
            
        #create the finalized dict, and push it into the main leaderboard array
        leaderboard = {'id': gameid, 'name': game['name'], 'value_header': value_header, 'player_scores': player_scores}
        leaderboards.append(leaderboard)

    return render_template('leaderboards.html', leaderboards=leaderboards)