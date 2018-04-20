#!/usr/bin/python3

'''
Created on Apr 19, 2018

@author: fabian
'''

from flask import Flask, render_template
from flask_socketio import SocketIO
from collections import OrderedDict, namedtuple

app = Flask(__name__)
socket = SocketIO(app)

PUZZLE_FILE = "answers.csv"

Puzzle = namedtuple("Puzzle",["puzzle_name", "puzzle_answer"])
solved_puzzles = []

puzzle_answers = OrderedDict()


def readFile():
    with open(PUZZLE_FILE) as f:
        for line in f:
            if line == "":
                break
            name,answer = line.strip().split("|")
            puzzle_answers[name] = answer
            solved_puzzles.append(Puzzle(name,answer))
    solved_puzzles.sort()
            
@app.route("/")
def index():
    return str(solved_puzzles)


if __name__ == '__main__':
    readFile()
    socket.run(app,host="0.0.0.0", port=3467)