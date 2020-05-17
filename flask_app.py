from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import sys
class Person(db.Model):
   __tablename__ = 'persons'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(), nullable=False)
   def __repr__(self):
      print (self.name)
      return f"<Person ID here: str({self.id}), {self.name}>"    
    
db.create_all()

results = Person.query.filter_by(name='Bob').all()
print(results)
print('here')

@app.route('/')
def indef():
    person = Person.query.first()
    #person = Person()
    #person.__repr__()
    #return 'Hello1 ' + person.__repr__()
    return 'Hi ' + person.name + ' ' + str(person.id)

#def repr():
#   person = Person.query(name='Amy')
#   return person.name + ' ' + person.id
print(sys.path)
