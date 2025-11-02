from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.debug = True
    app.secret_key = "somesecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitedata.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Bootstrap5(app)

# Flask-Login 
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"   # redirect here if not logged in
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.scalar(db.select(User).where(User.id == int(user_id)))

    # Blueprints 
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)




    # Error Handling
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        try:
            db.session.rollback()
        except Exception:
            pass
        return render_template('500.html'), 500
    
    return app
