from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
   __tablename__ = 'persons'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(), nullable=False)

db.create_all()

@app.route('/')
def indef():
    person = Person.query.first()
    return 'Hello ' + person.name
