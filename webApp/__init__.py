from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


#Starting SQL ALchemy
db = SQLAlchemy()
#The Database name
DB_NAME = "database.db"
#Just to remove notifications
SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_database(app):
    #If the Database does not exist, create it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def create_app():
    # Settings for the Server
    app = Flask(__name__)
    # Remove Rand Error
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret Key
    app.config['SECRET_KEY'] = 'FFFFFF111111fadasdfFFZZzz1'
    # Link the Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Initiating the Database
    db.init_app(app)

    # Import from Views ( Website Events )
    from .views import views
    # Import from Auth ( User and Authenficiation )
    from .auth import auth

    # Connect both blueprint to all the "url" in the next folder (templates)
    #Back-end
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import Database from Models ( User & Note )
    from .models import User, Note

    #Check if Database Exist Function
    create_database(app)

    #Starting the Login Manager. Login Backend
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #This sets the callback for reloading a user from the session.
    #The function you set should take a user ID (a unicode) and return a user object,
    #or None if the user does not exist.

    #Getting the User ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app



