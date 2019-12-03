from flask import Flask, render_template, request, session, redirect, jsonify

import database
import security

import random

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

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

@app.route('/answer/', methods=['POST'])
def awnser():
    if request.method == 'POST':
        awnserSubmited = request.form.get("ans")
        qn = request.form.get("q")
        if qn == 23:
            return 's'
        for n, i in enumerate(range(21)):
            if open("questions.txt", 'r').read().split('\n')[i].split("||")[1] == str(awnserSubmited) and str(n) == str(qn):
                return 'true'
            elif str(n) == str(qn):
                break
        return False

@app.route('/points/', methods=['POST'])
def checkPoints():
    if request.method == 'POST':
        return str(session.get("player"+str(request.form.get("player")))[3])

@app.route("/getQs/", methods=['POST'])
def nnnQuest():
    q = request.form.get("q")
    for n, i in enumerate(open("questions.txt", "r").read().split('\n')):
        print(n, q)
        if str(n) == str(q):
            temp = open("questions.txt", "r").read().split('\n')[random.randint(0, 21)].split('||')[1]
            temp1 = open("questions.txt", "r").read().split('\n')[random.randint(0, 21)].split('||')[1]
            while temp == temp1 or temp == i.split('||')[0] or temp1 == i.split('||')[0]:
                temp = open("questions.txt", "r").read().split('\n')[random.randint(0, 21)].split('||')[1]
                temp1 = open("questions.txt", "r").read().split('\n')[random.randint(0, 21)].split('||')[1]
            try: temp = str(i.split('||')[1]+'||'+temp+'||'+temp1).split('||')
            except: return 'done'
            random.shuffle(temp, random.random)
            if i.split('||')[0] == 'done':
                return i
            return i.split('||')[0]+'||'+'||'.join(temp)
    return 'done'



@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', e=e)

@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', e=e)

if __name__ == '__main__':
    app.secret_key = bytes(random.randint(1, 100000))
    app.run(debug=True, port=3000)
