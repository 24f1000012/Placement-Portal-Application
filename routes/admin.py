from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from utils.decorators import admin_required
from services.admin_service import AdminService

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = AdminService.get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/companies')  
@admin_required
def showCompanies():
    search_type = request.args.get('search_type')
    search_query = request.args.get('search_query')
    
    companies = []
    
    if search_query:
        # Search based on type
        if search_type == 'name':
            success, result = AdminService.get_company_by_name(search_query)
            companies = result if success else []
        elif search_type == 'industry':
            success, result = AdminService.get_company_by_industry(search_query)
            # get_company_by_industry returns a list already
            companies = result if success else []
        
        if not companies:
            flash(f'No companies found for "{search_query}"', 'warning')
    else:
        # No search - show all companies
        companies = AdminService.get_all_companies()
    
    return render_template("admin/companies.html", companies=companies)

@admin_bp.route("/company/<int:company_id>/approve", methods=['POST'])  
@admin_required
def approveCompany(company_id):
    success, message = AdminService.approve_company(company_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showCompanies"))  

@admin_bp.route("/company/<int:company_id>/reject", methods=['POST'])  
@admin_required
def rejectCompany(company_id):
    success, message = AdminService.reject_company(company_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showCompanies"))  

@admin_bp.route('/students')  
@admin_required
def showStudents():
    search_type = request.args.get('search_type')
    search_query = request.args.get('search_query')
    students = []
    if search_query:
        if search_type == 'name':
            success, result = AdminService.get_student_by_name(search_query)
            students = result if success else []
        elif search_type == 'roll':
            success, result = AdminService.get_student_by_roll(search_query)
            students = [result] if success else []
        elif search_type == 'contact':
            success, result = AdminService.get_student_by_contact(search_query)
            students = [result] if success else []
        if not students:
            flash(f'No students found for "{search_query}"', 'warning')
    else:
        students = AdminService.get_all_students()
    return render_template("admin/students.html", students=students)

@admin_bp.route('/students/<int:student_id>/blacklist', methods=['POST'])  
@admin_required
def blacklistStudent(student_id):
    success, message = AdminService.blacklist_student(student_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showStudents"))

@admin_bp.route('/students/<int:student_id>/unblacklist', methods=['POST'])  
@admin_required
def unblacklistStudent(student_id):
    success, message = AdminService.unblacklist_student(student_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showStudents"))


@admin_bp.route('/drives')  
@admin_required
def showDrives():
    """View all placement drives"""
    # Optional: filter by status using query param
    status = request.args.get('status')  # ?status=pending
    drives = AdminService.get_all_drives(status)
    return render_template("admin/drives.html", drives=drives)

@admin_bp.route('/drive/<int:drive_id>/approve', methods=['POST'])  
@admin_required
def approveDrive(drive_id):
    """Approve a placement drive"""
    success, message = AdminService.approve_drive(drive_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showDrives"))

@admin_bp.route('/drive/<int:drive_id>/reject', methods=['POST'])  
@admin_required
def rejectDrive(drive_id):
    """Reject a placement drive"""
    success, message = AdminService.reject_drive(drive_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showDrives"))

@admin_bp.route('/applications')
@admin_required
def manageApplications():
    from models import Application

    applications = Application.query\
        .order_by(Application.applied_date.desc())\
        .all()

    return render_template(
        "admin/applications.html",
        applications=applications
    )