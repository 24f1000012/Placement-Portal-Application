# routes/company.py
from flask import Blueprint, render_template, session, redirect, url_for

# Create blueprint
company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/dashboard')
def dashboard():
    # Check if user is company
    if session.get('role') != 'company':
        return redirect(url_for('auth.login'))
    
    return render_template('company/dashboard.html')
