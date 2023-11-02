from flask import Flask, render_template, url_for, flash, request, redirect, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
import sqlite3
import alak # the alak playing model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    model_moves = [0, 1]
    return render_template('game.html', model_moves=model_moves)

@app.route('/move/<int:old>/<int:new>/<board>')
def get_move(old, new, board):
    game = alak.Alak(moveX='interactive', moveO='model', print_result=True)
    json = game.getNext(old, new, board)

    return json

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, user, pswd):
        self.id = str(id)
        self.user = user
        self.pswd = pswd
        self.authenticated = False
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def get_id(self):
        return self.id

@app.route('/signIn')
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('login.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where user = (?)", [form.user.data])
        user = list(curs.fetchone())
        Us = load_user(user[0])
        if form.user.data == Us.user and form.pswd.data == Us.pswd:
            user(Us, remember=form.remember.data)
            userName = list({form.user.data})[0]
            flash('Logged in successfully ' + userName)
            redirect(url_for('game'))
        else:
            flash('Login Unsuccessfull.')
    return render_template('signIn.html',title='signIn', form=form)

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

if __name__ == "__main__":
    app.run()