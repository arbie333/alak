from flask import Flask, render_template, Blueprint
from . import db
from flask_login import login_required, current_user
import project.alak # the alak playing model

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required

def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/game')
def game():
    model_moves = [0, 1]
    return render_template('game.html', model_moves=model_moves)

@main.route('/move/<int:old>/<int:new>/<board>')
def get_move(old, new, board):
    game = project.alak.Alak(moveX='interactive', moveO='model', print_result=True)
    json = game.getNext(old, new, board)

    return json

@main.route('/record')
def record():
    return render_template('record.html')

@main.route('/ranking')
def ranking():
    return render_template('ranking.html')

if __name__ == "__main__":
    main.run()