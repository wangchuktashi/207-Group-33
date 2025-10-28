from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.debug = True
    app.secret_key = "somesecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitedata.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Bootstrap5(app)

    login_manager.init_app(app)

    from . import views
    app.register_blueprint(views.mainbp)
    return app


from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
