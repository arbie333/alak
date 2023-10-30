# @app.route('/')
# def dynamic_page():
#     return play.official_games('o')

# cockie session

# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# import sqlite3
import test_api
import sys
from flask import Flask, render_template, Blueprint
import numpy as np

import alak # the alak playing model

app = Flask(__name__)

# api test
if test_api.test_blueprint not in sys.modules:
    if isinstance(test_api.test_blueprint, Blueprint):
        app.register_blueprint(test_api.test_blueprint)

# the model
# if alak.alak_blueprint not in sys.modules:
#     if isinstance(alak.alak_blueprint, Blueprint):
#         app.register_blueprint(alak.alak_blueprint, url_prefix='/game')

@app.route('/')
def index():
    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    # conn.close()
    return render_template('index.html')

@app.route('/game')
def game():
    model_moves = [0, 1]
    return render_template('game.html', model_moves=model_moves)

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/move/<int:old>/<int:new>/<board>')
def get_move(old, new, board):
    game = alak.Alak(moveX='interactive', moveO='model', print_result=True)
    json = game.getNext(old, new, board)

    return json

if __name__ == "__main__":
    app.run()