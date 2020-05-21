from flask import Flask, jsonify, os
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    cors = CORS(app, resource={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return 'GETTING MESSAGES'
        
    if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile('config.py', silent=True)
    else:
      # load the test config if passed in
      app.config.from_mapping(test_config)

    @app.route('/')
    def hello():
      return jsonify('message Hello world')
      
    
    return app 