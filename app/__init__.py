from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/monitoria_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "secret"

    db.init_app(app)
    login_manager.init_app(app)
    from app import routes
    routes.init_app(app)
    return app

#Create_app factory da class Flask
#onde db abstrai a factory de rotas e passa a classe mãe app