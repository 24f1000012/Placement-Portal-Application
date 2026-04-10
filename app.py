from flask import Flask, render_template
from config import Config
from models import db
from services.auth_service import AuthService  # ← Import service
from routes.company import company_bp
from routes.admin import admin_bp
from routes.student import student_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        AuthService.create_default_admin()  # ← Use service
    
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.company import company_bp
    from routes.student import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)
    
    return app

app = create_app()

@app.route('/', methods=['GET'])
def home():
    return render_template('log.html')

if __name__ == '__main__':
    app.run(debug=True)