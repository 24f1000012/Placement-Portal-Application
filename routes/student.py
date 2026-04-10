from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from utils.decorators import student_required
from services.student_services import StudentService
from config import Config
from models import Application
student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@student_required
def dashboard():
    user_id = session.get('user_id')
    student = StudentService.get_student_by_user_id(user_id)

    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('auth.login'))

    stats = StudentService.get_student_stats(student.id)
    recent_updates = Application.query\
    .filter_by(student_id=student.id)\
    .order_by(Application.applied_date.desc())\
    .limit(5)\
    .all()

    return render_template(
        'student/dashboard.html',
        student=student,
        stats=stats,
        recent_updates=recent_updates
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    user_id = session.get('user_id')
    student = StudentService.get_student_by_user_id(user_id)

    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name       = request.form.get('name')
        phone      = request.form.get('phone')
        department = request.form.get('department')
        cgpa       = request.form.get('cgpa')
        skills     = request.form.get('skills')
        resume_file = request.files.get('resume')

        success, message = StudentService.update_profile(
            student.id, name, phone, department,
            cgpa, skills, resume_file, Config.UPLOAD_FOLDER
        )

        flash(message, 'success' if success else 'danger')

        if success:
            return redirect(url_for('student.profile'))

    return render_template('student/profile.html', student=student)


@student_bp.route('/jobs')
@student_required
def browse_jobs():
    user_id = session.get('user_id')
    student = StudentService.get_student_by_user_id(user_id)

    search_type  = request.args.get('search_type')
    search_query = request.args.get('search_query')

    drives = StudentService.get_approved_drives(search_query, search_type)

    if search_query and not drives:
        flash(f'No jobs found for "{search_query}"', 'warning')

    from models import Application
    applied_drive_ids = [
        app.drive_id for app in
        Application.query.filter_by(student_id=student.id).all()
    ]

    return render_template(
        'student/jobs.html',
        drives=drives,
        student=student,
        applied_drive_ids=applied_drive_ids
    )


@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
@student_required
def apply(drive_id):
    user_id = session.get('user_id')
    student = StudentService.get_student_by_user_id(user_id)

    success, message = StudentService.apply_to_drive(student.id, drive_id)
    flash(message, 'success' if success else 'danger')

    return redirect(url_for('student.browse_jobs'))


@student_bp.route('/applications')
@student_required
def my_applications():
    user_id = session.get('user_id')
    student = StudentService.get_student_by_user_id(user_id)

    applications = StudentService.get_student_applications(student.id)

    return render_template(
        'student/my_applications.html',
        student=student,
        applications=applications
    )