import os

from flask import Flask
from flask_cors import CORS

import json

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'illdriveus.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # try to load the test configuration
    if test_config is None:
        # load the instance config, if it exists, when not testing
        config_path = os.path.join(app.instance_path, 'config.json')
        config = json.load(open(config_path, 'r'))
        app.config.update(config)
    else:
        # load the test config if passed in
        app.config.update(test_config)



    # register the database commands
    from . import db
    db.init_app(app)

    # apply the blueprints to the app
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')


    # Apply CORS rules to the entire application
    # IMHO it's not worth configuring properly ATM
    CORS(app, origin='*')

    return app
