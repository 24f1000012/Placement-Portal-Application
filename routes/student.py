# routes/student.py
from flask import Blueprint, render_template, session, redirect, url_for

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
def dashboard():
    # Check if user is student
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    return render_template('student/dashboard.html')
