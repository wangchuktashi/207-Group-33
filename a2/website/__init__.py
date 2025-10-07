from flask import Flask

def create_app():
    print(__name__)            # will print 'website'
    app = Flask(__name__)

     # REGISTER BLUEPRINTS
    from .views import mainbp
    app.register_blueprint(mainbp) 
    
    return app
