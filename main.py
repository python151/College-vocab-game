from flask import Flask, render_template, request

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

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', e=e)

@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', e=e)

if __name__ == '__main__':
    app.secret_key = random.randint(1, 100000)
    app.run(debug=True, port=3000)