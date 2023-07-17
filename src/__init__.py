from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Creating a Database Instance and DB name
db = SQLAlchemy()
DB_NAME = "database.db"


def flask_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ncajebfcBDBVJDBHVbdchdbvjadvkBBHBAHDJHV'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Telling the DB which app we are using
    db.init_app(app)

    from .views import views
    from .auth import auth

    #Registering the blueprints with the main app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()

    #Login Manager's Login View and route
    login_manager.login_view = 'auth.login'

    #Telling the login manager which app we are using
    login_manager.init_app(app)

    #Login Manager loads user when the flask app login completed
    @login_manager.user_loader
    def load_user(id):
        #This user Query BY default it looks for primary key which is id, we need not to specify id=='some id'
        return User.query.get(int(id))

    return app
