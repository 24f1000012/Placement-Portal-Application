from flask import Flask
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()          # Creates all tables
        create_admin(app)        # Creates default admin

    return app

def create_admin(app):
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_user = User(
                email    = 'admin@placement.com',
                password = generate_password_hash('admin123'),
                role     = 'admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin created: admin@placement.com / admin123")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)