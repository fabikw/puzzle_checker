#!/usr/bin/python3

'''
Created on Apr 19, 2018

@author: fabian
'''

from collections import OrderedDict, namedtuple
from pathlib import Path
import os
from flask import Flask, render_template, redirect, flash
from flask_socketio import SocketIO, emit
from flask_wtf import FlaskForm
from flask_wtf import csrf
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import datetime

def get_now():
    return datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")


app = Flask(__name__)
socket = SocketIO(app)

PUZZLE_FILE = "answers.csv"
CORRECT_PUZZLES = "correct.txt"
total = 0
solved = 0

Puzzle = namedtuple("Puzzle",["puzzle_name", "puzzle_answer", "solved_time"])
solved_puzzles = []

puzzle_answers = OrderedDict()

# class Config(object):
#     WTF_CSRF_ENABLED = False
#     
# app.config.from_object(Config)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "fafafritas"


class CheckAnswer(FlaskForm):
    puzzle_list = SelectField(label = "Puzzle Name:")
    answer = StringField(label = "Answer:",validators=[DataRequired()])
    submit = SubmitField(label = "Check answer")


def readFile():
    global solved_puzzles, puzzle_answers, total, solved
    with open(PUZZLE_FILE) as f:
        for line in f:
            if line == "":
                break
            name,answer = line.strip().split("|")
            puzzle_answers[name] = answer
            #solved_puzzles.append(Puzzle(name,answer))
    total = len(puzzle_answers)
    Path(CORRECT_PUZZLES).touch()
    with open(CORRECT_PUZZLES) as f:
        for line in f:
            try:
                line, time = line.strip().split("|")
                solved_puzzles.append(Puzzle(line, puzzle_answers[line],time))
                del puzzle_answers[line]
            except:
                pass
    solved = len(solved_puzzles)
            
@app.route("/", methods=["GET","POST"])
@app.route("/index", methods = ["GET","POST"])
def index():
    global solved_puzzles, puzzle_answers, solved, total
    form = CheckAnswer()
    form.puzzle_list.choices = zip(puzzle_answers.keys(), puzzle_answers.keys())
    if form.validate_on_submit():
        puzzle = form.puzzle_list.data
        answer = form.answer.data.upper().replace(" ", "")
        if answer == puzzle_answers[puzzle]:
            now = get_now()
            solved_puzzles.append(Puzzle(puzzle,answer,now))
            with open(CORRECT_PUZZLES,"a") as f:
                f.write(puzzle+"|"+now+"\n")
            del puzzle_answers[puzzle]
            solved += 1
            emit("puzzle solved", broadcast=True, namespace="/test")
        else:
            flash("{} is an incorrect answer for {}".format(answer, puzzle))
        return redirect("/index")
    form.puzzle_list.choices = zip(puzzle_answers.keys(), puzzle_answers.keys())
    return render_template("index.html", solved_list = solved_puzzles, form = form, solved = solved, total = total)


if __name__ == '__main__':
    readFile()
    socket.run(app,host="0.0.0.0", port=3467,debug = True)