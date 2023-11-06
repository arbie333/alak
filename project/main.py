from flask import Flask, render_template, Blueprint
from . import db
from .models import Record, User
from flask_login import login_required, current_user
import project.alak # the alak playing model
from datetime import date
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/game')
def game():
    try:
        displayed_name = current_user.name
    except:
        displayed_name = "our guest"
    return render_template('game.html', name=displayed_name)

@main.route('/move/<int:old>/<int:new>/<board>/<time>')
def get_move(old, new, board, time):
    game = project.alak.Alak(moveX='interactive', moveO='model', print_result=True)
    jsonStr = game.getNext(old, new, board)
    res = json.loads(jsonStr)

    if res['win'] != 0:
        addRecord(res, time)

    return jsonStr

def addRecord(json, seconds):
    # second string to time string
    min = int(seconds) // 60
    sec = int(seconds) % 60
    timeStr = "{}:{}".format(min, sec)
    print('seconds', seconds)
    print('timeStr', timeStr)

    # result
    if json['win'] == 1:
        res = "WIN"
    else:
        res = "LOSE"
    try:
        user = User.query.filter_by(name=current_user.name).first()
        record = Record(user_id=user.id, user_name=user.name, time=timeStr, result=res, date=date.today().strftime("%d/%m/%Y"))
        db.session.add(record)
        db.session.commit()
    except:
        print('record of guest will not be documented')

@main.route('/record')
def record():
    record = Record.query.filter_by(user_name=current_user.name).order_by(Record.date).limit(10).all()
    print(record[0].time)
    return render_template('record.html', name=current_user.name, result=record)

@main.route('/ranking')
def ranking():
    try:
        displayed_name = current_user.name
    except:
        displayed_name = "our guest"
    record = Record.query.filter_by(result="WIN").order_by(Record.time).limit(10).all()
    return render_template('ranking.html', result=record, name=displayed_name)

if __name__ == "__main__":
    main.run()