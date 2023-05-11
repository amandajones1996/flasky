from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# grabs enviroment variables
from dotenv import load_dotenv
# reads enviroment variables
import os
# gives us access to database operations
db = SQLAlchemy()
migrate = Migrate()
# load the values from our env file so the os module can see them
load_dotenv()

def create_app(test_config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    # stop tracking of the files
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # set up database
    if not test_config:
        # environ is a method from os that returns a dictionary
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY__TEST_DATABASE_URI")
    # connect the db and migrate to our app 
    db.init_app(app)
    migrate.init_app(app, db)

    # import routes
    from .routes import crystal_bp, healer_bp
    # registar the blueprint
    app.register_blueprint(crystal_bp)
    app.register_blueprint(healer_bp)

    from app.models.crystal import Crystal 
    from app.models.healer import Healer
    return app