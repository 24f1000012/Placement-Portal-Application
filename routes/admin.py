from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils.decorators import admin_required
from services.admin_service import AdminService

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = AdminService.get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/companies')  # ← Changed from /dashboard/companies
@admin_required
def showCompanies():
    companies = AdminService.get_all_companies()
    return render_template("admin/companies.html", companies=companies)

@admin_bp.route("/company/<int:company_id>/approve", methods=['POST'])  # ← Fixed path
@admin_required
def approveCompany(company_id):
    success, message = AdminService.approve_company(company_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showCompanies"))  # ← Fixed url_for

@admin_bp.route("/company/<int:company_id>/reject", methods=['POST'])  # ← Fixed path
@admin_required
def rejectCompany(company_id):
    success, message = AdminService.reject_company(company_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for("admin.showCompanies"))  # ← Fixed url_for