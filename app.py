#%%
import datetime as dt
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # !export DATABASE_URL=$(heroku config:get DATABASE_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gyoqwfjsduneih:87d63380e16241bb8b244798c7ce53b2055b50c7bcf92a9b3a626dc11d30e781@ec2-75-101-232-85.compute-1.amazonaws.com:5432/dcspke83naf934'

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = 'comment'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    comment = db.Column(db.Text())

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
        data = request.get_json()
        db.session.add(Comment(data['name'], data['comment']))
        db.session.commit()
    comments = Comment.query.all()
    return {
        comment._id: {
            'name':comment.name, 
            'comment':comment.comment
        } for comment in comments
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0')