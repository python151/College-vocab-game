from flask import Flask, render_template, request, session, redirect

import database
import security

import random

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

class Player:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.questionNumber = 1
        self.points = 100

class questions:
    def get(qnumber):
        allQuestions = open('questions.txt', 'r')
        questionsInFormat = allQuestions.read().split("\n")
        for q in questionsInFormat:
            if qnumber == q.split("|")[1]:
                return q
    def awnser(number, awnser):
        allQuestions = open('questionAwnsers.txt', 'r')
        questionsInFormat = allQuestions.read().split("\n")
        for q in questionsInFormat:
            if number == q.split("|")[1]:
                if awnser == q.split("|")[0]:
                    return True
                else:
                    return False

app = Flask(__name__)

# NO MORE CACHING
app.config['SEND_FILE_AGE_DEFAULT'] = 0

# Logging user ip
@app.before_request
def log():
    Base = declarative_base()
    engine = create_engine('sqlite:///database.db', poolclass=SingletonThreadPool)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    s=DBSession()
    new_log = database.Log(endpoint=str(request.endpoint), ip=str(request.remote_addr))
    s.add(new_log)
    s.commit()


# Home Page or Index Page
@app.route('/Home')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/howtoplay')
def learn():
    return render_template("rules.html")

@app.route('/game')
def game():
    session['score'] = 100
    session['turn'] = 1
    return render_template('game.html')

@app.route("/update_score/")
def update_score():
    increment = request.form.get('increment')
    session['score'] += increment
    return 'success'

@app.route('/restart')
def restart():
    session[''] = ''
    return redirect("/game")

@app.route('/readyupplayer/', methods=['POST'])
def readyup():
    number = request.form.get("playerNumber")
    name = request.form.get("playerName")
    session['player'+str(number)] = [name, number, 1, 100]
    return 'success'

@app.route('/awnser/', methods=['POST'])
def awnser():
    if request.method == 'POST':
        awnserSubmited = request.form.get("awnser")
        player = request.form.get("player")
        qNumber = session.get("player"+player)[2]
        playerObj = session.get("player"+str(player))
        if questions.awnser(qNumber, awnserSubmited):
            playerObj.points[3] += 10
            playerObj[2] += 1
            return questions.get(playerObj.questionNumber)
        else:
            playerObj[3] -= 10
        return 'incorrect'

@app.route('/points/', methods=['POST'])
def checkPoints():
    if request.method == 'POST':
        return str(session.get("player"+str(request.form.get("player")))[3])




@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', e=e)

@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', e=e)

if __name__ == '__main__':
    app.secret_key = bytes(random.randint(1, 100000))
    app.run(debug=True, port=3000)