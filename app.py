#%%
import datetime as dt
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
import os
import psycopg2
import pytz

app = Flask(__name__)
CORS(app)

ENV = 'prod'
if ENV == 'dev':
    os.system("export FLASK_ENV=development")
    if 'DATABASE_URL' not in os.environ:
        from subprocess import Popen
        os.environ['DATABASE_URL'] = Popen('echo $(heroku config:get DATABASE_URL)',shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")[:-1]
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = 'comment'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    comment = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime, default=dt.datetime.utcnow)

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f'{self.name} says, "{self.comment}"' 

#%%
@app.route('/')
def index():
    return 'Hello! route to /comments to view comments, or POST one yourself and see them all with body like {"name":____,"comment":___}'


@app.route('/comments', methods=['GET','POST'])
def comments():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        db.session.add(Comment(data['name'], data['comment']))
        db.session.commit()
    comments = Comment.query.all()        
    return {
        comment._id: {
            'name':comment.name, 
            'comment':comment.comment,
            'created_date':comment.created_date.replace(tzinfo=dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
        } for comment in comments
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=(ENV=='dev'))