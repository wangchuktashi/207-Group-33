from website import db, create_app
import website.models  # ensure models are registered

app = create_app()
with app.app_context():
    print("DB URI:", db.engine.url)
    db.create_all()
    print("Tables created.")
