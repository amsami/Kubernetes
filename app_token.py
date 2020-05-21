#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sqlalchemy
import os
from functools import wraps
from jose import jwt
from urllib.request import urlopen

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
from datetime import datetime
#db.create_all() 

# AK TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

AUTH0_domain = ''
Algorithms = ['RS256']
API_AUDIENCE = 'image'

Class AuthError(Exception):
   def __init__(self, error, status_code)
      self.error = EnvironmentError
      self.status_code = status_code

#def verify_decode_jwt(token):
#    jsonurl = urlopen(f'https://{AUTH0_domin/.well-known')
#    jwks = json.loads


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        print('hereee')
        abort(401)

    auth_header = request.headers['Authorization']
    header_auth = auth_header.split(' ')
    
    if len (header_auth) != 2:
        print('here')
        abort(401)
    elif header_auth[0].lower() != 'bearer':
        print('yes')
        abort(401)
    
    return header_auth[1]

def requires_auth(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    jwt = get_token_auth_header()
    return f(jwt, *args, **kwargs)
  return wrapper  

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

@app.route('/headers')
@requires_auth
def headers(jwt):
    print(jwt)
    return 'not implemented'