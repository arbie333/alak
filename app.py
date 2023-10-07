import sqlite3
from flask import Flask, render_template
import play # the alak playing model

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def dynamic_page():
    return play.official_games('o')

@app.route('/')
def index():
    conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
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