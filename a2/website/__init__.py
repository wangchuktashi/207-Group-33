from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.debug = True
    app.secret_key = "somesecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitedata.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Bootstrap5(app)

    from . import views
    app.register_blueprint(views.mainbp)
    return app
