#!/usr/bin/python3

'''
Created on Apr 19, 2018

@author: fabian
'''

from flask import Flask, render_template, redirect
from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from flask_wtf import csrf
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from collections import OrderedDict, namedtuple

app = Flask(__name__)
socket = SocketIO(app)

PUZZLE_FILE = "answers.csv"

Puzzle = namedtuple("Puzzle",["puzzle_name", "puzzle_answer"])
solved_puzzles = []

puzzle_answers = OrderedDict()

class Config(object):
    WTF_CSRF_ENABLED = False
    
app.config.from_object(Config)

class CheckAnswer(FlaskForm):
    puzzle_list = SelectField(label = "Puzzle Name:")
    answer = StringField(label = "Answer:",validators=[DataRequired()])
    submit = SubmitField(label = "Check answer")


def readFile():
    with open(PUZZLE_FILE) as f:
        for line in f:
            if line == "":
                break
            name,answer = line.strip().split("|")
            puzzle_answers[name] = answer
            #solved_puzzles.append(Puzzle(name,answer))
    solved_puzzles.sort()
            
@app.route("/", methods=["GET","POST"])
@app.route("/index", methods = ["GET","POST"])
def index():
    global solved_puzzles, puzzle_answers
    form = CheckAnswer()
    form.puzzle_list.choices = zip(puzzle_answers.keys(), puzzle_answers.keys())
    if form.validate_on_submit():
        puzzle = form.puzzle_list.data
        answer = form.answer.data.upper().replace(" ", "")
        if answer == puzzle_answers[puzzle]:
            solved_puzzles.append(Puzzle(puzzle,answer))
            del puzzle_answers[puzzle]
        return redirect("/index")
    return render_template("index.html", solved_list = solved_puzzles, form = form)


if __name__ == '__main__':
    readFile()
    socket.run(app,host="0.0.0.0", port=3467,debug = True)