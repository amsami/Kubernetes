if test_config is None:
 # load the instance config, if it exists, when not testing
 app.config.from_pyfile('config.py', silent=True)
else:
 # load the test config if passed in
 app.config.from_mapping(test_config)