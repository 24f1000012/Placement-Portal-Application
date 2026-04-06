from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import company_required
from services.company_service import CompanyService
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/dashboard')
@company_required
def dashboard():
    user_id = session.get('user_id')
    company = CompanyService.get_company_by_user_id(user_id)
    
    if not company:
        flash('Company profile not found', 'danger')
        return redirect(url_for('auth.login'))
    
    stats = CompanyService.get_company_stats(company.id)
    
    return render_template('company/dashboard.html', company=company, stats=stats)

@company_bp.route('/create_drive', methods=['GET', 'POST'])
@company_required
def create_drive():
    if request.method == 'POST':
        user_id = session.get('user_id')
        company = CompanyService.get_company_by_user_id(user_id)
        
        # Get form data
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        eligibility = request.form.get('eligibility')
        salary = request.form.get('salary')
        location = request.form.get('location')
        deadline_str = request.form.get('application_deadline')
        
        # Convert deadline string to datetime
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except:
                flash('Invalid deadline format', 'danger')
                return render_template('company/create_drive.html')
        
        # Call service
        success, message = CompanyService.create_drive(
            company.id, job_title, job_description,
            eligibility, salary, location, deadline
        )
        
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('company.dashboard'))
    
    return render_template('company/create_drive.html')

@company_bp.route('/drives')
@company_required
def view_drives():
    user_id = session.get('user_id')
    company = CompanyService.get_company_by_user_id(user_id)
    
    drives = CompanyService.get_company_drives(company.id)
    
    return render_template('company/drives.html', drives=drives, company=company)