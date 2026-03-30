# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data (HTTP layer responsibility)
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Call service for business logic
        success, user, message = AuthService.authenticate_user(email, password)
        
        if success:
            # Create session (HTTP layer responsibility)
            session['user_id'] = user.id
            session['role'] = user.role
            
            flash('Welcome back!', 'success')
            
            # Redirect based on role (HTTP layer responsibility)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company.dashboard'))
            else:  # student
                return redirect(url_for('student.dashboard'))
        else:
            # Show error message
            flash(message, 'danger')
    
    # GET request - show login form
    return render_template('login.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Call service for business logic
        success, message = AuthService.register_student(email, password, name)
        
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    
    # GET request - show registration form
    return render_template('register_student.html')


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        
        # Call service for business logic
        success, message = AuthService.register_company(email, password, company_name)
        
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    
    # GET request - show registration form
    return render_template('register_company.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))