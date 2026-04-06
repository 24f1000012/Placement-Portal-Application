# utils/decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Access denied: Admin only', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'company':
            flash('Access denied: Company only', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function